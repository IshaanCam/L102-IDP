import config
import utime
from machine import Pin, I2C
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from navigation import turn

#NEED TO IMPORT THE SIDE REALLY:


# --- Setup TOF Sensor ---
i2c_bus = I2C(id=0, sda=Pin(20), scl=Pin(21), freq=100000)
tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

def init_tof():
    while tof.begin() != 0:
        utime.sleep(0.1)
    tof.start_measurement(calib_m=tof.eMODE_NO_CALIB, mode=tof.eDISTANCE) #Distance Mode

def is_bay_empty():
    """Returns True if distance is > Threshold (no box present)"""
    while not tof.is_data_ready():
        utime.sleep(0.01)
    dist = tof.get_distance_mm()
    return dist > config.BAY_DISTANCE_THRESHOLD_MM

def deliver_sequence(side):
    init_tof()
    j_crossed = 0

    while True:
    # We are currently at a junction (stopped)
        if is_bay_empty():
            print("Space empty")
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR)

            config.LEFT_MOTOR.Forward(config.BASE_SPEED)
            config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            utime.sleep(1.0)

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
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
                        
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR) 

            while j_crossed > 0:
                # Move forward to rejoin the line
                config.LEFT_MOTOR.Forward(config.BASE_SPEED)
                config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
                utime.sleep(0.2)
                config.LF = True
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
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