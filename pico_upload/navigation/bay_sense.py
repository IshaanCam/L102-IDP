import utility.config as config
import utime
from machine import Pin, I2C
from navigation.turn import turn
from libs.VL53L0X.VL53L0X import VL53L0X

# --- Setup TOF Sensors ---

i2c_bus_vl53_right = I2C(id=1, sda=Pin(10), scl=Pin(11)) #right hand ToF sensor initialised on I2C1
i2c_bus_vl53_left = I2C(id=0, sda=Pin(8), scl=Pin(9)) #left hand ToF sensor initialised on I2C0
vl53l0_r = VL53L0X(i2c_bus_vl53_right)
vl53l0_l = VL53L0X(i2c_bus_vl53_left)

#   -------------------------------------

def init_tof(side: str) -> None:
    """
    Completes the initialisation of the appropriate ToF sensor

    Args:
    - side (str): Whether the right or left hand sensor needs to be initialised


    """

    if side == "right":
         
        vl53l0_r.set_Vcsel_pulse_period(vl53l0_r.vcsel_period_type[0], 18)
        vl53l0_r.set_Vcsel_pulse_period(vl53l0_r.vcsel_period_type[1], 14)

        vl53l0_r.start()
    if side == "left":
        vl53l0_l.set_Vcsel_pulse_period(vl53l0_l.vcsel_period_type[0], 18)
        vl53l0_l.set_Vcsel_pulse_period(vl53l0_l.vcsel_period_type[1], 14)

        vl53l0_l.start()
    

def is_bay_empty(side: str) -> bool:
    """
    Reads the distance from the appropriate ToF sensor

    Args:
    - side (str): Whether the right or left hand sensor needs to be initialised


    """
    
    if side == "right":
        dist = vl53l0_r.read() # get sensor data
        while (dist < 0) or (dist > 7000): #An error reads -1 and initialise value is a maximum of 8000. Hence, keep reading until a real value is read
            dist = vl53l0_r.read()
            utime.sleep(0.003)
        return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000 # Return whether the distance is below a threshold (distance to full bay)
    else: # same as right hand side but for the left hand side sensor
        dist = vl53l0_l.read()
        while (dist < 0) or (dist > 7000):
            dist = vl53l0_r.read()
            utime.sleep(0.003)
        return dist > config.BAY_DISTANCE_THRESHOLD_MM and dist < 1000

    

def deliver_sequence(side: str) -> None:
    """
    A function that travels through the bays and turns into the first empty one. If none are found empty
    for any reason, it turns into the last one

    Args:
    - side (str): Which side the bays will be


    """
    init_tof(side) #initialise the appropriate sensor
    j_crossed = -1 #Number of junctions crossed while finding empty bay.
                   #During AGV turn it skips a junction, hence j_crossed initialised as -1

    while True:
    # We are currently at a junction (stopped)
        if is_bay_empty(side) or j_crossed > 4: #If a bay is empty of we are at the 6th bay
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR) #turns into the bay, depending on side


            config.SERVO2.Turn(60) #Lift the arms up so that the box can be put inside the bay
            utime.sleep(0.6) #Let the AGV travel into the bay
            config.LEFT_MOTOR.Stop() #Stop to deliver
            config.RIGHT_MOTOR.Stop()
            
            config.SERVO1.Turn(30) #Open the arms to drop reel
            utime.sleep(0.2)
            config.SERVO2.Turn(40) #Bring arms back down

            # Drop_box()

            # Reverse out of the bay
                
            config.RIGHT_MOTOR.Reverse(config.BASE_SPEED) #reverse out of the bay
            config.LEFT_MOTOR.Reverse(config.BASE_SPEED)
            
            while not config.JUNCTION_DETECTED: #detect the junction from which we entered
                utime.sleep(0.003)
            config.JUNCTION_DETECTED = False
            turn(side, config.RIGHT_MOTOR, config.LEFT_MOTOR) #Turn back out
            config.JUNCTION_DETECTED = False
            while j_crossed > 0: #Keep skipping junctions until you have crossed the same never as you did while enterning
                                 # Ensures smooth exit from bays 
                # Move forward to until the next junction is detected
                config.LEFT_MOTOR.Forward(config.BASE_SPEED)
                config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
                utime.sleep(0.2)
                config.LF = True
                while not config.JUNCTION_DETECTED:
                    utime.sleep(0.003)
                config.JUNCTION_DETECTED = False
                config.LF = False
                j_crossed -= 1
            
            config.SERVO1.Turn(10) #Open the arms fully again ready for the next reel
            break #Exit finding empty bay algorithm

        else:
            j_crossed += 1 #If the bay is not empty add another junction crossed
            config.LEFT_MOTOR.Forward(config.BASE_SPEED) #Move forward until the next bay is detected
            config.RIGHT_MOTOR.Forward(config.BASE_SPEED)
            utime.sleep(0.2)
            config.LF = True
            while not config.JUNCTION_DETECTED:
                utime.sleep(0.003)
            config.LF = False
            config.JUNCTION_DETECTED = False
            config.LEFT_MOTOR.Stop()
            config.RIGHT_MOTOR.Stop()
            utime.sleep(0.1)
            


