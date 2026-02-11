import utility.config as config
import utime
from machine import Pin, I2C
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from navigation.turn import turn, turn_180
from libs.VL53L0X.VL53L0X import VL53L0X

# --- Setup TOF Sensors ---

i2c_bus_vl53_left = I2C(id=0, sda=Pin(), scl=Pin())
i2c_bus_vl53_right = I2C(id=1, sda=Pin(), scl=Pin())
vl53l0_left = VL53L0X(i2c_bus_vl53_left)
vl53l0_right = VL53L0X(i2c_bus_vl53_right)

#   -------------------------------------

def init_tof(side):
    if side == 'left':
        vl53l0_left.set_Vcsel_pulse_period(vl53l0_left.vcsel_period_type[0], 18)
        vl53l0_left.set_Vcsel_pulse_period(vl53l0_left.vcsel_period_type[1], 14)

        vl53l0_left.start()

    elif side == "right":
         
        vl53l0_right.set_Vcsel_pulse_period(vl53l0_right.vcsel_period_type[0], 18)
        vl53l0_right.set_Vcsel_pulse_period(vl53l0_right.vcsel_period_type[1], 14)

        vl53l0_right.start()
    

def is_bay_empty(side):
    """Returns True if distance is > Threshold (no box present)"""
    if side == 'left':
        dist = vl53l0_left.read()
        print(dist)
        return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000
    
    elif side == 'right':
        dist = vl53l0_right.read()
        print(dist)
        return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000


def deliver_sequence(side, back_to_start=True):
    """ Tests if bays are empty on the side input given, delivers box to the first empty bay and then returns to original position in reverse orientation.
    If it overshoots all the bays it will turn around and try again facing the other direction - with back_to_start = False and then if it finds an empty
    bay it will drop off and return to the original start position in reverse orientation.
    
    Only error if it doesnt sense an empty space either time then it will continue to attempt to on the return journey but cba to do smthg to stop that"""

    init_tof(side)
    j_crossed = 0

    while True:
    # We are currently at a junction (stopped)
        if j_crossed >= 6: #Overshot too many junctions - missed the open bay - turning around and trying again. If because overrides empty bay test
            print("Too many junctions crossed, turning around...")
            turn_180("left", config.RIGHT_MOTOR, config.LEFT_MOTOR)
            config.LEFT_MOTOR.Forward(60) #get to first bay as we are currently at the fake tape junction
            config.RIGHT_MOTOR.Forward(60)
            utime.sleep(0.2)
            config.LF = True
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.LF = False
            config.JUNCTION_DETECTED = False
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
            if side == 'left':
                side = 'right'
            elif side == 'right':
                side = 'left'

            deliver_sequence(side, False)

        elif is_bay_empty(side):
            print("Space empty")
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR)

            #config.LEFT_MOTOR.Forward(config.BASE_SPEED)
            #config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            #utime.sleep(0)

            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()

            # Drop_box()
            print("Box Dropped")
            utime.sleep(1)

            # Reverse out of the bay
            config.LEFT_MOTOR.Reverse(config.BASE_SPEED)
            config.RIGHT_MOTOR.Reverse(config.BASE_SPEED)
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.JUNCTION_DETECTED = False

            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR) 

            if back_to_start:          
                while j_crossed > 0:
                    # Move forward to rejoin the line
                    config.LEFT_MOTOR.Forward(config.BASE_SPEED)
                    config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
                    utime.sleep(0.2)
                    config.LF = True
                    while not config.JUNCTION_DETECTED:
                        utime.sleep(0.003)
                    config.JUNCTION_DETECTED = False
                    config.LF = False
                    j_crossed -= 1
            
                print("Back to original position in reverse orientation")
                break
            
            else:
                while j_crossed < 5:
                    # Move forward to rejoin the line
                    config.LEFT_MOTOR.Forward(config.BASE_SPEED)
                    config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
                    utime.sleep(0.2)
                    config.LF = True
                    while not config.JUNCTION_DETECTED:
                        utime.sleep(0.003)
                    config.JUNCTION_DETECTED = False
                    config.LF = False
                    j_crossed += 1
                
                print("Have overshot, turned around, dropped off on other side and then returned back to original position in reverse orientation")
                break          

        else:  
            j_crossed += 1
            print("Bay occupied, moving to next junction...")
            config.LEFT_MOTOR.Forward(60)
            config.RIGHT_MOTOR.Forward(60)
            utime.sleep(0.2)
            config.LF = True
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.LF = False
            config.JUNCTION_DETECTED = False
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
            utime.sleep(1)
