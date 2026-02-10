from machine import Pin
class LineTracker(): 
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)
        pass
    
    def read_value(self):
        return self.pin.value()