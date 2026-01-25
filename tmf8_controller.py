from utime import sleep
from machine import Pin, I2C

from libs.DFRobot_TMF8x01 import DFRobot_TMF8701

def test_TMF8x01_get_distance():
    # Both options work
    # i2c_bus = SoftI2C(sda=Pin(8), scl=Pin(9), freq=100000)  # I2C0 on GP8 & GP9
    i2c_bus = I2C(sda=Pin(8), scl=Pin(9), freq=100000) # I2C0 on GP8 & GP9
    #print(i2c_bus.scan()) # 65=0x41
    assert len(i2c_bus.scan()) == 1 # This demo requires exactly one device

    tof = DFRobot_TMF8701(i2c_bus=i2c_bus)

    print("Initialising ranging sensor TMF8701......")
    while(tof.begin() != 0):
      print("   Initialisation failed")
      sleep(0.5)
    print("   Initialisation done.")

    print("Software Version: ", end=" ")
    print(tof.get_software_version())
    print("Unique ID: %X"%tof.get_unique_id())
    print("Model: ", end=" ")
    print(tof.get_sensor_model())

    '''
    @brief Config measurement params to enable measurement. Need to call stop_measurement to stop ranging action.
    @param calib_m: Is an enumerated variable of , which is to config measurement cailibration mode.
    @n     eMODE_NO_CALIB  :          Measuring without any calibration data.
    @n     eMODE_CALIB    :          Measuring with calibration data.
    @n     eMODE_CALIB_AND_ALGOSTATE : Measuring with calibration and algorithm state.
    @param mode : the ranging mode of TMF8701 sensor.
    @n     ePROXIMITY: Raing in PROXIMITY mode,ranging range 0~10cm
    @n     eDISTANCE: Raing in distance mode,ranging range 10~60cm
    @n     eCOMBINE:  Raing in PROXIMITY and DISTANCE hybrid mode,ranging range 0~60cm
    @return status:
    @n      false:  enable measurement failed.
    @n      true:  enable measurement sucess.
    '''

    tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.ePROXIMITY)
    #tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.eCOMBINE)
    #tof.start_measurement(calib_m = tof.eMODE_NO_CALIB, mode = tof.eDISTANCE)

    while True:
      if(tof.is_data_ready() == True):
        print(f"Distance = {tof.get_distance_mm()} mm (make sure you read about mode selection above!)")
      sleep(0.5)
