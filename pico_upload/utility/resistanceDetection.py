from machine import ADC, Pin
from utime import sleep

def blink(led, times=10, interval=0.1):
    for _ in range(times):
        led.value(1)
        sleep(interval)
        led.value(0)
        sleep(interval)

def resistancedetect():
    voltage = ADC(28)
    sleep(1)
    val = voltage.read_u16()
    
    blueled = Pin(0, Pin.OUT)
    greenled = Pin(1, Pin.OUT)
    redled = Pin(3, Pin.OUT)
    yellowled = Pin(2, Pin.OUT)

    if (val > 800) and (val < 5000):
        print("Blue LED blinking")
        blink(blueled)

    elif (val > 6000) and (val < 30000):
        print("Green LED blinking")
        blink(greenled)
    
    elif (val > 34000) and (val < 40000):
        print("Red LED blinking")
        blink(redled)

    elif (val > 40000) and (val < 50000):
        print("Yellow LED blinking")
        blink(yellowled)

