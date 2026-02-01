from motorController import Motor
from sensors.line_tracking import LineTracker

BASE_SPEED = 90
JUNCTION_DETECTED = False
JUNCTION_ARMED = True
LF = True
prev_pos = 0
states = [
    'pre-pickup_move',
    # 'pick_up_box',
    # 'pre-delivery_move',
    # 'deliver_box'
]

bays = [
    'bay_3',
    # 'bay_4',
    # 'bay_1',
    # 'bay_2',
]

RIGHT_MOTOR = Motor()
LEFT_MOTOR = Motor()

FAR_RIGHT_SENSOR = LineTracker(13)
CENTER_RIGHT_SENSOR = LineTracker(12)
CENTER_LEFT_SENSOR = LineTracker(11)
FAR_LEFT_SENSOR = LineTracker(10)

LINE_SENSOR = [
    FAR_LEFT_SENSOR, 
    CENTER_LEFT_SENSOR, 
    CENTER_RIGHT_SENSOR,
    FAR_RIGHT_SENSOR,
]

WEIGHTS = [
    -2, -1, 1, 2
]

pid_controls = {
    "Kp" : 30,
    "Ki" : 0,
    "Kd" : 20,
}

WEIGHTS = [-2, -1, 1, 2] #  These will be used for finding our centroid (negative for left, positive for right)