from machine import ADC
from utime import sleep

voltage = ADC(26)

while True:
    val = voltage.read_u16()
    print(val)
    sleep(0.1)
