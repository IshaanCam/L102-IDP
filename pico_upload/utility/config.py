from controllers.motorController import Motor
from controllers.servoController import Servo
from sensors.line_tracking import LineTracker
from navigation.PID import PID
from machine import Pin

# Configuration file to store environment variables

BASE_SPEED = 95
JUNCTION_DETECTED = False
JUNCTION_ARMED = True
LF = False
BAY_DISTANCE_THRESHOLD_MM = 300
prev_pos = 0
states = [
    'pre-pickup_move',
    'pick_up_box',
    'pre-delivery_move',
    'deliver_box'
] #state machine for navigation

bays = [
    "bay_3",
    "bay_4",
    'bay_1',
    'bay_2',
] #bays to be looped through in navigation algorithm

LEDS = {
    "blue": Pin(0, Pin.OUT),
    "green": Pin(1, Pin.OUT),
    "yellow": Pin(2, Pin.OUT),
    "red": Pin(3, Pin.OUT)
} #Initialising all the LEDS


#Initialising the motors
RIGHT_MOTOR = Motor(7, 6)
LEFT_MOTOR = Motor(4, 5)

#Initialising the servos
SERVO1 = Servo(15)
SERVO2 = Servo(13)

#Initialising the line sensors
FAR_RIGHT_SENSOR = LineTracker(21)
CENTER_RIGHT_SENSOR = LineTracker(22)
CENTER_LEFT_SENSOR = LineTracker(20)
FAR_LEFT_SENSOR = LineTracker(19)

LINE_SENSOR = [
    FAR_LEFT_SENSOR, 
    CENTER_LEFT_SENSOR, 
    CENTER_RIGHT_SENSOR,
    FAR_RIGHT_SENSOR,
]

pid_controls = {
    "Kp" : 30,
    "Ki" : 0,
    "Kd" : 0,
}

#Initialising the pid controller
pid = PID(Kp = pid_controls['Kp'], Ki = pid_controls['Ki'], Kd=pid_controls['Kd'], output_limits=(-50, 50))

WEIGHTS = [-2, -1, 1, 2] #  These will be used for finding our centroid (negative for left, positive for right)
