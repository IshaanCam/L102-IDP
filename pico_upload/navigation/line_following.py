import utility.config as config

# WHITE IS HIGH

def centroid_position(vals: list[int], weights: list[int]) -> tuple[float | None, int]:
    """
    Calculates the centroid position based on the position weights and sensor values.

    Args:
    - vals (list[int]): A list containing the sensor vals
    - weights (list[int]): The weights for each of the line sensors

    Returns:
    - tuple[float| None, int]: Returns the position and the sum of all sensor vals
    """

    val_weight_sum = 0
    val_sum = 0

    #Loop through each sensor val and its weight
    for vi, wi in zip(vals, weights):
        val_weight_sum += (vi) * wi #Compute a weighted sum
        val_sum += (vi) #Compute a sum
    
    if val_sum == 0: #If the sum in 0, then a divide by 0 error occurs. Return None to avoid
        return None, 0
    
    return val_weight_sum / val_sum, val_sum #Return position as the ratio of weighted sum and total sum and the total sum

def line_following(
        timer
    ) -> None:
    """
    Function reads inputs from the light sensors and uses a weighted approach to calculate deviation from the centroid. It then uses
    a PID controller to fix the said error
    
    Args
    - timer: Place holder object for the timer instance

    """
    base_speed = config.BASE_SPEED

    if config.LF: #Check if we are meant to be line following

        sensor_vals = [sensor.read_value() for sensor in config.LINE_SENSOR] #Read the values from all from line sensors

        pos, sum = centroid_position(sensor_vals, config.WEIGHTS) #Calculate the offset of the AGV from the center of the line

        if pos is None: #When a T-junction detected, we get a divide by 0 hence None is returned. In this case assume last non 0 position
            pos = config.prev_pos


        e = -pos # Convert the position into an error
        
        config.prev_pos = pos  # storing in case of T junction detected
        correction = config.pid.update(e) #Use PID controller to get a speed correction term
        

        cmd_left = base_speed - correction # Turn one wheel faster and the other slower depending on direction of error to get back on course
        cmd_right = base_speed + correction

        cmd_left = max(0, min(100, cmd_left)) #Ensure the wheel velocities do not breach 0 - 100 which causes motor faults
        cmd_right = max(0, min(100, cmd_right))

        config.LEFT_MOTOR.Forward(cmd_left) #Set the corrected velocities
        config.RIGHT_MOTOR.Forward(cmd_right)
        
    return 

