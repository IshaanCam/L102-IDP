# from sensors.line_tracking import LineTracker
import config
import random as random

def junction_detecter(timer):
    # if ((left_sensor.read_value() == 1) or (right_sensor.read_value() == 1)):
    #     junction_detected = True
    # else:
    #     junction_detected = False
    rn = random.randint(1, 5)
    if rn == 1:
        config.JUNCTION_DETECTED = True
    else:
        config.JUNCTION_DETECTED = False
    print(f'{config.JUNCTION_DETECTED}, junction_detector')