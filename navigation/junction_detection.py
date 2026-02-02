# from sensors.line_tracking import LineTracker
import config

def junction_detecter(timer):
    # if config.JUNCTION_TICKER > 0:
    #     config.JUNCTION_TICKER -= 1
    #     return
    if config.JUNCTION_ARMED:
        if (
            ((config.FAR_LEFT_SENSOR.read_value() == 1) and (config.CENTER_LEFT_SENSOR.read_value() == 1)) or
            ((config.FAR_RIGHT_SENSOR.read_value() == 1) and (config.CENTER_RIGHT_SENSOR.read_value() == 1))
            ):
            config.JUNCTION_DETECTED = True
            config.JUNCTION_ARMED = False
            config.LF = False
            # config.JUNCTION_TICKER = config.JUNCTION_COOLDOWN
    else: 
        if ((config.FAR_LEFT_SENSOR.read_value() == 0) and (config.FAR_RIGHT_SENSOR.read_value() == 0)):
            config.JUNCTION_ARMED = True
    # rn = random.randint(1, 5)
    # if rn == 1:
    #     config.JUNCTION_DETECTED = True
    # else:
    #     config.JUNCTION_DETECTED = False
    # print(f'{config.JUNCTION_DETECTED}, junction_detector')
