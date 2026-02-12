import utility.config as config
import utime
from machine import Pin, I2C
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from navigation.turn import turn
from libs.VL53L0X.VL53L0X import VL53L0X
from navigation.turn import turn_180
#NEED TO IMPORT THE SIDE REALLY:

# --- Setup TOF Sensors ---

#i2c_bus_vl53_right = I2C(id=1, sda=Pin(10), scl=Pin(11))
i2c_bus_vl53_left = I2C(id=0, sda=Pin(8), scl=Pin(9))
#vl53l0_r = VL53L0X(i2c_bus_vl53_right)
vl53l0_l = VL53L0X(i2c_bus_vl53_left)

#   -------------------------------------

def init_tof(side):
    #if side == 'left':
        
        #while tof.begin() != 0:
            #utime.sleep(0.1)
        #tof.start_measurement(calib_m=tof.eMODE_NO_CALIB, mode=tof.eDISTANCE) #Distance Mode

    #if side == "right":
         
        #vl53l0_r.set_Vcsel_pulse_period(vl53l0_r.vcsel_period_type[0], 18)
        #vl53l0_r.set_Vcsel_pulse_period(vl53l0_r.vcsel_period_type[1], 14)

        #vl53l0_r.start()
    if side == "left":
        vl53l0_l.set_Vcsel_pulse_period(vl53l0_l.vcsel_period_type[0], 18)
        vl53l0_l.set_Vcsel_pulse_period(vl53l0_l.vcsel_period_type[1], 14)

        vl53l0_l.start()
    

def is_bay_empty(side):
    """Returns True if distance is > Threshold (no box present)"""
    #if side == 'left':
        #while not tof.is_data_ready():
            #utime.sleep(0.01)
        #dist = tof.get_distance_mm()
        #print(dist)
        #return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000
    
    #if side == "right":
        #dist = vl53l0_r.read()
        #print(dist)
        #return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000
    if side == "left":
        dist = vl53l0_l.read()
        print(dist)
        return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000

    

def deliver_sequence(side):
    init_tof(side)
    j_crossed = -1

    while True:
    # We are currently at a junction (stopped)
        if is_bay_empty(side):
            print("Space empty")
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR)

            #config.LEFT_MOTOR.Forward(config.BASE_SPEED)
            #config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            #utime.sleep(0)
            utime.sleep(0.20)
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
            
            utime.sleep(1)

            # Drop_box()

            # Reverse out of the bay
            turn_180("left", config.RIGHT_MOTOR, config.LEFT_MOTOR)
            config.RIGHT_MOTOR.Stop()
            config.LEFT_MOTOR.Stop()
                
            config.RIGHT_MOTOR.Reverse(60)
            config.LEFT_MOTOR.Reverse(60)
            utime.sleep(0.5)
            config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            config.LEFT_MOTOR.Forward(config.BASE_SPEED)
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.JUNCTION_DETECTED = False
            if side == "left":       
                turn("right", config.RIGHT_MOTOR, config.LEFT_MOTOR)
            else:
                turn("left", config.RIGHT_MOTOR, config.LEFT_MOTOR)
            config.JUNCTION_DETECTED = False
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
            j_crossed += 1
            print("Bay occupied, moving to next junction...")
            config.LEFT_MOTOR.Forward(config.BASE_SPEED)
            config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            utime.sleep(0.2)
            config.LF = True
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.LF = False
            config.JUNCTION_DETECTED = False
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
            utime.sleep(1)


