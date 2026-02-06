from motorController import Motor
from sensors.line_tracking import LineTracker
# from fakeStuff import FakeLineSensor, FakeMotor, FakeJunctionSensor
from PID import PID

# Actual program

BASE_SPEED = 80
JUNCTION_DETECTED = False
JUNCTION_ARMED = True
LF = False
BAY_DISTANCE_THRESHOLD_MM = 200
prev_pos = 0
states = [
    'pre-pickup_move',
    'pick_up_box',
    'pre-delivery_move',
    # 'deliver_box'
]

bays = [
    "bay_3",
    "bay_4",
    # 'bay_1',
    # 'bay_2',
]

RIGHT_MOTOR = Motor(7, 6)
LEFT_MOTOR = Motor(4, 5)

FAR_RIGHT_SENSOR = LineTracker(28)
CENTER_RIGHT_SENSOR = LineTracker(27)
CENTER_LEFT_SENSOR = LineTracker(1)
FAR_LEFT_SENSOR = LineTracker(2)

#LEFT_SIDE_SENSOR = 
#RIGHT_SIDE_SENSOR = 

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
    "Kp" : 100,
    "Ki" : 0,
    "Kd" : 80,
}

pid = PID(Kp = pid_controls['Kp'], Ki = pid_controls['Ki'], Kd=pid_controls['Kd'], output_limits=(-50, 50))

WEIGHTS = [-2, -1, 1, 2] #  These will be used for finding our centroid (negative for left, positive for right)

# Fake program for testing
# BASE_SPEED = 60

# LEFT_MOTOR = FakeMotor("LEFT")
# RIGHT_MOTOR = FakeMotor("RIGHT")

# LINE_SENSOR = [
#     FakeLineSensor([0,1,1,1,0]),
#     FakeLineSensor([1,1,1,1,0]),
#     FakeLineSensor([1,1,1,1,0]),
#     FakeLineSensor([0,1,1,0,0]),
# ]

# FAR_LEFT_SENSOR = FakeJunctionSensor([# start → j1
#     0,0,0,0,
#     1,1,0,0,
#     # j1 → bay_3_entrance
#     0,1,1,0,0,
#     # bay_3_entrance → bay_4_entrance
#     0,0,0,0,0,
#     # entrance_lower_b
#     0,0,0,1,0,0,
#     # exit_lower_b
#     0,1,0,
#     # back_right_corner
#     0,1,0,
#     # ramp
#     0,0,1,1,0,
#     # back_left_corner
#     0,1,0,
#     # exit_lower_a
#     0,1,0,
#     # entrance_lower_a
#     0,0,1,0,
#     # bay_1_entrance
#     0,1,0,
#     # bay_2_entrance
#     0,0,0,
#     # return to start
#     0,0,0,0,0,0])
# FAR_RIGHT_SENSOR = FakeJunctionSensor([# start → j1
#     0,0,0,0,
#     1,1,0,0,
#     # j1 → bay_3_entrance
#     0,1,1,0,0,
#     # bay_3_entrance → bay_4_entrance
#     0,0,1,1,0,
#     # entrance_lower_b
#     0,0,0,1,0,0,
#     # exit_lower_b
#     0,0,0,
#     # back_right_corner
#     0,0,0,
#     # ramp
#     0,0,0,0,0,
#     # back_left_corner
#     0,0,0,
#     # exit_lower_a
#     0,0,0,
#     # entrance_lower_a
#     0,0,0,0,
#     # bay_1_entrance
#     0,0,0,
#     # bay_2_entrance
#     0,1,0,
#     # return to start
#     0,0,1,1,0,0])

# WEIGHTS = [-2, -1, 1, 2]

# pid = PID(Kp=25, Ki=0, Kd=6, output_limits=(-40, 40))

# prev_pos = 0
# LF = True
# JUNCTION_DETECTED = False
# JUNCTION_ARMED = True
# JUNCTION_COOLDOWN = 5
# JUNCTION_TICKER = 0
