import utility.config as config

def junction_detecter(timer):
    """
    Uses the line sensors to see if the AGV has reached a junction. config.JUNCTION_ARMED added to stop the same
    junction being detected twice

    Args:
    - timer: placeholder variable for the timer instance
    """
    if config.JUNCTION_ARMED: #Checking to see if the AGV has definitely moved away from the previous junction
        if (
            ((config.FAR_LEFT_SENSOR.read_value() == 1) and (config.CENTER_LEFT_SENSOR.read_value() == 1)) or
            ((config.FAR_RIGHT_SENSOR.read_value() == 1) and (config.CENTER_RIGHT_SENSOR.read_value() == 1))
            ): #If either the left two sensors or the right two sensors detect white, then we have reached a junction
            config.JUNCTION_DETECTED = True
            config.JUNCTION_ARMED = False #Stop same junction being detected again
            config.LF = False #Preparing for turning
    else: 
        if ((config.FAR_LEFT_SENSOR.read_value() == 0) and 
            (config.FAR_RIGHT_SENSOR.read_value() == 0)): #Once both outer sensors see black, we have moved on from the junction
            config.JUNCTION_ARMED = True #Get ready to start detecting junctions again
