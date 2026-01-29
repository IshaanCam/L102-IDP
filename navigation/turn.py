def turn(direction: str, right_motor, left_motor, junction_detected) -> None:
    right_motor.Stop()
    left_motor.Stop()
    motor = right_motor
    if direction == "left":
        motor = left_motor
    while not junction_detected:
        if direction == "right":
            motor.Forward()
        else:
            motor.Forward()
    motor.Stop()