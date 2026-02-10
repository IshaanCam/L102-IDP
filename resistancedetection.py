from machine import ADC, Pin
from utime import sleep

def blink(led, times=10, interval=0.1):
    for _ in range(times):
        led.value(1)
        sleep(interval)
        led.value(0)
        sleep(interval)

def resistancedetect():
    voltage = ADC(26)
    val = voltage.read_u16()
    print(val)
    sleep(0.1)
    
    blueled = Pin(28, Pin.OUT)
    greenled = Pin(27, Pin.OUT)
    redled = Pin(1, Pin.OUT)
    yellowled = Pin(0, Pin.OUT)

    if (val > 800) and (val < 1200):
        print("Blue LED blinking")
        blink(blueled)

    elif (val > 6000) and (val < 8000):
        print("Green LED blinking")
        blink(greenled)
    
    elif (val > 34000) and (val < 38000):
        print("Red LED blinking")
        blink(redled)

    elif (val > 42000) and (val < 44000):
        print("Yellow LED blinking")
        blink(yellowled)



resistancedetect()



