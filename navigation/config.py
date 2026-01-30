from motorController import Motor
from sensors.line_tracking import LineTracker

BASE_SPEED = 90
junction_detected = False
lf = False
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

FAR_RIGHT_SENSOR = LineTracker()
CENTER_RIGHT_SENSOR = LineTracker()
CENTER_LEFT_SENSOR = LineTracker()
FAR_LEFT_SENSOR = LineTracker()
