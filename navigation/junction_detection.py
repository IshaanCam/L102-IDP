# from sensors.line_tracking import LineTracker
import config
import random as random

def junction_detecter(timer):
    if config.JUNCTION_ARMED:
        if ((config.FAR_LEFT_SENSOR.read_value() == 1) or (config.FAR_RIGHT_SENSOR.read_value() == 1)):
            config.JUNCTION_DETECTED = True
            config.JUNCTION_ARMED = False
    else: 
        if ((config.FAR_LEFT_SENSOR.read_value() == 0) and (config.FAR_RIGHT_SENSOR.read_value() == 0)):
            config.JUNCTION_ARMED = True
    # rn = random.randint(1, 5)
    # if rn == 1:
    #     config.JUNCTION_DETECTED = True
    # else:
    #     config.JUNCTION_DETECTED = False
    # print(f'{config.JUNCTION_DETECTED}, junction_detector')