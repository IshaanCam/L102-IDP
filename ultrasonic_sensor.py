from utime import sleep
from machine import Pin, I2C

def test_ultrasonic_sensor():
    i2c_bus = I2C(sda=Pin(8), scl=Pin(9), freq=100000) #Set up an I2C bus on GPIO8&9
    assert len(i2c_bus.scan()) == 1

    [addr] = i2c_bus.scan()

    while True:
        data = i2c_bus.readfrom_mem(addr, int('0x03', base=16), 2) #Read two bytes from the sensor starting at the register 0x03
        distance = (data[0] << 8) | data[1]
        print(distance)
        sleep(0.5)