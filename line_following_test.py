from navigation.junction_info import junction_info as path
from navigation.path import path as to_and_fro
from utime import sleep
from navigation.turn import turn

def line_following_test(junction_detected, right_motor, left_motor):
    position = ('start', 'start')
    while not junction_detected:
        sleep(0.05)
    junction_detected = False
    movement = to_and_fro[position]
    for junction in movement:
        while not junction_detected:
            sleep(0.05)
        if path[junction][position] != "forward":
            turn(path[junction][position], right_motor, left_motor, junction_detected)
        junction_detected = False