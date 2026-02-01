from machine import Pin
import random as random
class LineTracker(): 
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)
        pass
    
    def read_value(self):
        return self.pin.value()