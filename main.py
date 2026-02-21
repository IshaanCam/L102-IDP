from machine import Pin, PWM, Timer
import utime
import utility.config as config
from utility.path import path as to_and_fro
from navigation.line_following import line_following
from navigation.junction_detection import junction_detecter
from navigation.bay_sense import deliver_sequence
from navigation.turn import turn, turn_180
from utility.resistanceDetection import resistancedetect

# Dictionary with information of what to do at each node depending on starting and ending location
# Key: nodes
# Value: Dict {
    # Key: (start, end)
    # Value: movement directive
#}
path = {
    "start": {
        ("start", "bay_3"): "forward",
        ("lower_b", "start"): "forward",
        ("lower_a", "start"): "forward",
        ("upper_b", "start"): "forward",
        ("upper_a", "start"): "forward",
        ("start", "start"): "forward",
    },
    "j1": {
        ("bay_3", "lower_a"): "forward", 
        ("bay_4", "lower_a"): "forward", 
        ("lower_b", "bay_1"): "forward", 
        ("lower_b", "bay_2"): "forward",
        ("start", "bay_3"): "right", 
        ("lower_a", "bay_4"): "forward", 
        ("bay_2", "lower_b"): "forward",
        ("bay_1", "lower_b"): "forward",
        ("lower_a", "start"): "right",
        ("upper_a", "start"): "right",
        ("lower_b", "start"): "left",
        ("upper_b", "start"): "left",
        ("start", "start"): "right"
    },
    "bay_3_entrance": {
        ("bay_3", "lower_a"): "left", 
        ("bay_4", "lower_a"): "forward", 
        ("bay_3", "lower_b"): "right",
        ("bay_3", "upper_b"): "right",
        ("bay_3", "upper_a"): "right",
        ("lower_b", "bay_1"): "forward", 
        ("lower_b", "bay_2"): "forward",
        ("start", "bay_3"): "right", 
        ("lower_a", "bay_4"): "forward", 
        ("bay_2", "lower_b"): "forward",
        ("bay_1", "lower_b"): "forward",
        ("lower_b", "start"): "forward",
        ("upper_b", "start"): "forward",
        ("start", "start"): "forward"
    },
    "bay_4_entrance": {
        ("bay_4", "lower_a"): "left", 
        ("bay_3", "lower_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_3", "upper_a"): "left",
        ("lower_b", "bay_1"): "right", 
        ("lower_b", "bay_2"): "right",
        ("lower_b", "bay_4"): "forward",
        ("upper_b", "bay_4"): "forward",
        ("lower_a", "bay_4"): "right", 
        ("upper_a", "bay_4"): "forward",
        ("bay_2", "lower_b"): "left",
        ("bay_1", "lower_b"): "left",
        ("lower_b", "start"): "right",
        ("upper_b", "start"): "right",
        ("bay_4", "lower_b"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("start", "start"): "left"
    },
    "back_right_corner": {
        ("bay_3", "upper_a"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_a"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_a", "bay_4"): "right",
        ("upper_b", "bay_4"): "right",
        ("start", "start"): "left"
    },
    "ramp": {
        ("bay_3", "upper_a"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_a"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_a", "bay_4"): "right",
        ("upper_b", "bay_4"): "right",
        ("upper_a", "bay_1"): "left",
        ("upper_b", "bay_1"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_b", "bay_2"): "left",
        ("bay_1", "upper_a"): "right",
        ("bay_1", "upper_b"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_2", "upper_b"): "right",
        ("start", "start"): "forward"
    },
    "back_left_corner": {
        ("upper_a", "bay_1"): "left",
        ("upper_b", "bay_1"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_b", "bay_2"): "left",
        ("bay_1", "upper_a"): "right",
        ("bay_1", "upper_b"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_2", "upper_b"): "right",
        ("start", "start"): "left"
    },
    "entrance_lower_b": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b2": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b3": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b4": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b5": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_b6": {
        ("bay_3", "upper_a"): "forward",
        ("bay_3", "upper_b"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "exit_lower_b": {
        ("upper_a", "bay_4"): "forward",
        ("upper_b", "bay_4"): "forward",
        ("bay_3", "upper_a"): "forward",
        ("bay_4", "upper_a"): "forward",
        ("bay_4", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "top_of_ramp": {
        ("bay_1", "upper_a"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_3", "upper_a"): "right",
        ("bay_4", "upper_a"): "right",
        ("bay_1", "upper_b"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_b", "bay_4"): "right",
        ("upper_b", "bay_2"): "right",
        ("upper_b", "bay_1"): "right",
        ("upper_a", "bay_4"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "left"
    },
    "corner_before_upper_b": {
        ("bay_1", "upper_b"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_3", "upper_b"): "left",
        ("bay_4", "upper_b"): "left",
        ("upper_b", "bay_4"): "right",
        ("upper_b", "bay_2"): "right",
        ("upper_b", "bay_1"): "right"
    },
    "corner_before_upper_a": {
        ("bay_1", "upper_a"): "right",
        ("bay_2", "upper_a"): "right",
        ("bay_3", "upper_a"): "right",
        ("bay_4", "upper_a"): "right",
        ("upper_a", "bay_4"): "left",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "left"
    },
    "entrance_lower_a": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a2": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a3": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a4": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a5": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "entrance_lower_a6": {
        ("bay_1", "upper_a"): "forward",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_a"): "forward",
        ("bay_2", "upper_b"): "forward",
        ("start", "start"): "forward"
    },
    "exit_lower_a": {
        ("upper_a", "bay_1"): "forward",
        ("upper_b", "bay_1"): "forward",
        ("upper_a", "bay_2"): "forward",
        ("upper_b", "bay_2"): "forward",
        ("start", "start"): "forward"
    },
    "bay_1_entrance": {
        ("bay_1", "lower_a"): "forward",
        ("bay_2", "lower_a"): "right", 
        ("bay_3", "lower_a"): "right",
        ("bay_4", "lower_a"): "right", 
        ("bay_1", "upper_a"): "forward",
        ("bay_2", "upper_a"): "right",
        ("bay_1", "upper_b"): "forward",
        ("bay_2", "upper_b"): "right",
        ("lower_a", "bay_4"): "left",
        ("lower_a", "bay_2"): "left",
        ("lower_a", "bay_1"): "forward",
        ("upper_a", "bay_2"): "left",
        ("upper_a", "bay_1"): "forward",
        ("upper_a", "start"): "left",
        ("lower_a", "start"): "left",
        ("upper_b", "bay_1"): "forward",
        ("upper_b", "bay_2"): "left",
        ("lower_b", "bay_1"): "left",
        ("bay_1", "lower_b"): "right",
        ("start", "start"): "left"
    },
    "bay_2_entrance": {
        ("bay_2", "lower_a"): "left",
        ("bay_2", "upper_a"): "left",
        ("bay_2", "upper_b"): "left",
        ("bay_2", "lower_b"): "right",
        ("bay_1", "lower_b"): "forward",
        ("bay_3", "lower_a"): "forward",
        ("bay_4", "lower_a"): "forward",
        ("lower_a", "start"): "forward",
        ("upper_a", "start"): "forward",
        ("lower_a", "bay_4"): "forward",
        ("lower_a", "bay_2"): "right",
        ("upper_a", "bay_2"): "right",
        ("upper_b", "bay_2"): "right",
        ("lower_b", "bay_2"): "left",
        ("lower_b", "bay_1"): "forward",
        ("start", "start"): "forward"
    }
}


# Main function combining all functionality
def main() -> None:
    start_position = "start"

    #Initialise button
    button_pin = 14
    button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

    #Initialise LED
    led = Pin(0, Pin.OUT)

    #Wait for a button press before starting functinon
    while not button.value():
        utime.sleep(0.003)
    
    #Initialise motors, servos and base speed
    left_motor = config.LEFT_MOTOR
    right_motor = config.RIGHT_MOTOR
    base_speed = config.BASE_SPEED
    config.SERVO1.Turn(10)
    config.SERVO2.Turn(40)

    #Begin moving forward
    left_motor.Forward(base_speed)
    right_motor.Forward(base_speed)

    #Set up timers for line_following and junction_dectection to run continously in the background and use config variables
    # to communicate and use their effects.
    Timer(mode=1, freq=200, callback=line_following)
    Timer(mode=1, freq=200, callback=junction_detecter)

    #Wait until you are at the end of the starting box before starting state machine
    while not config.JUNCTION_DETECTED:
        utime.sleep(0.003)
    config.JUNCTION_DETECTED = False
    for bay in config.bays:
        # Run through the bays in a pre-defined fashion. Not the fastest but lost time minimal and easiest to implement
        led.value(0)
        for st in config.states:
            # Start state machine for each pickup journey
            if st == "pre-pickup_move":

                #Use the node list defined in path.py to run through the junctions to hit
                position = (start_position, bay)
                movement = to_and_fro[position]
                config.LF = True
                for junction in movement:
                    while not config.JUNCTION_DETECTED: #wait until you hit the expected junction
                        utime.sleep(0.003)
                    config.LF = False #turn off line_following to allow effective turns
                    if path[junction][position] != "forward": #use the dictionary above to figure out what to do at the junction
                        turn(path[junction][position], right_motor, left_motor) #turn as required
                    else:
                        left_motor.Forward() #otherwise move forward
                        right_motor.Forward()
                        utime.sleep(0.2)
                    config.LF = True #restart line following for next junction
                    config.JUNCTION_DETECTED = False
                while not config.JUNCTION_DETECTED: #once all the junctions have been exhausted, the AGV is now just outside the pickup bays
                                                    #keep moving until you reach the pickup bays
                    utime.sleep(0.003)
                config.JUNCTION_DETECTED = False
                utime.sleep(0.2)
                right_motor.Stop() #stop and pass functionality to pickup algorithm
                left_motor.Stop()
            elif (st == "pick_up_box"):
                config.SERVO2.Turn(5) #Move the arms down
                config.SERVO1.Turn(55) #Clamp the arms onto the reel
                (led_color, delivery_location) = resistancedetect() #measure its resistance
                config.LEDS[led_color].value(1) #turn on the appropriate LED
                utime.sleep(0.5)
                config.SERVO2.Turn(40) # Raise the arms up
                if bay == "bay_1": #Due to the walls around the bays, the AGV can only spin in a specific direction. Turn the AGV 180 deg accordingly.
                    turn_180("right", right_motor, left_motor)
                elif bay == "bay_2":
                    turn_180("right", right_motor, left_motor)
                elif bay == "bay_3":
                    turn_180("left", right_motor, left_motor)
                elif bay == "bay_4":
                    turn_180("left", right_motor, left_motor)
                config.LF = True
            elif st == "pre-delivery_move": #Same as pre-pickup move. Drops the AGV at the first delivery rack
                position = (bay, delivery_location)
                movement = to_and_fro[position]
                for junction in movement:
                    while not config.JUNCTION_DETECTED:
                        utime.sleep(0.003)
                    config.LF = False
                    if path[junction][position] != "forward":
                        turn(path[junction][position], right_motor, left_motor)
                    else:
                        left_motor.Forward()
                        right_motor.Forward()
                        utime.sleep(0.2)
                    config.LF = True
                    config.JUNCTION_DETECTED = False
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                config.JUNCTION_DETECTED = False
                left_motor.Stop()
                right_motor.Stop()
                utime.sleep(1)
                start_position = delivery_location #set the delivery position as the start position for the next bay
            elif st == "deliver_box": #Execute the delivery sequence
                if delivery_location == "upper_a" or delivery_location == "lower_b": #The delivery rack defines which sensor gets used (the right or left)
                    deliver_sequence("left")
                else:
                    deliver_sequence("right")

    position = (delivery_location, "start") #Once all the racks have been covered, the AGV is now instructed to return from the delivery bay to start
    movement = to_and_fro[position]
    for junction in movement: #Movement algorithm exactly the same, running through junctions executing the tasks at each junction as required
        while not config.JUNCTION_DETECTED:
            utime.sleep(0.003)
        config.LF = False
        if path[junction][position] != "forward":
            turn(path[junction][position], right_motor, left_motor)
        else:
            left_motor.Forward()
            right_motor.Forward()
            utime.sleep(0.2)
        config.LF = True
        config.JUNCTION_DETECTED = False
    left_motor.Stop() #Once in the start box, stop
    right_motor.Stop()