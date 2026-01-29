from utime import sleep

def turn(direction: str, right_motor, left_motor) -> None:
    right_motor.Stop()
    left_motor.Stop()
    motor = right_motor
    if direction == "left":
        motor = left_motor
    if direction == "right":
        motor.Forward()
    else:
        motor.Forward()
    sleep(1)
    motor.Stop()