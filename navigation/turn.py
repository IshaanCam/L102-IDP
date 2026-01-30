# from utime import sleep
from time import sleep

def turn(direction: str, right_motor, left_motor) -> None:
    # right_motor.Stop()
    # left_motor.Stop()
    print('Stop')
    # motor = right_motor
    # if direction == "left":
    #     motor = left_motor
    if direction == "right":
        print('Right')
    else:
        print('Left')
    sleep(1)
    print('Stop')