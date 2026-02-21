from machine import Pin
class LineTracker():
    """
    Class for line sensors
    """ 
    def __init__(self, pin: int):
        """
        Initialise the line sensors

        Args:
        - pin (int): The pin number of the attached sensor
        """
        self.pin = Pin(pin, Pin.IN) #Set the pin object for the sensor
        pass
    
    def read_value(self):
        """
        Read sensor value
        """
        return self.pin.value() #Return the sensor value