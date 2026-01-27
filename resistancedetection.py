from machine import ADC
from utime import sleep

voltage = ADC(26)
val = voltage.read_u16()

while True:
    print(val)
    sleep(1)
