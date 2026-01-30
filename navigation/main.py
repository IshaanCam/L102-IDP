import config
# from config import FAR_LEFT_SENSOR, FAR_RIGHT_SENSOR, CENTER_RIGHT_SENSOR, CENTER_LEFT_SENSOR
from path_finder import path_finder
from junction_detection import junction_detecter
from line_following import line_following
from machine import Timer

def main():
    junction_detected = Timer(0, mode=Timer.PERIODIC, callback=junction_detecter, freq=200)
    lf = Timer(1, mode=Timer.PERIODIC, callback=line_following, freq=200)
    # junction_detecter(junction_detected)
    path_finder(config.RIGHT_MOTOR, config.LEFT_MOTOR, config.JUNCTION_DETECTED, config.bays, config.states, lf)
    # junction_timer = Timer(0, mode=Timer.PERIODIC, callback=junction_detecter, freq=1000)
    # # lf_timer = Timer(1, mode=Timer.PERIODIC, callback=line_following, freq=500)
    # path_finder(RIGHT_MOTOR, LEFT_MOTOR, JUNCTION_DETECTED, bays, states)
