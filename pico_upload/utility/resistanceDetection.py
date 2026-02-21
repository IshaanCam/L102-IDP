from machine import ADC, Pin
from utime import sleep

def resistancedetect() -> tuple[str, str]:
    """
    The function measures the resistance using a potential divider circuit. Based on measured thresholds it returns
    the right LED color and bay location
    """
    voltage = ADC(28) #Initialise ADC pin to read voltage
    sleep(5) # Wait to ensure proper contact and eliminate risks of short circuits
    val = voltage.read_u16() #Read the voltage

    #Return LED color, drop off location based on premeasured thresholds.

    if (val > 800) and (val < 5000):
        return ("blue", "upper_a")

    elif (val > 6000) and (val < 30000):
        return ("green", "lower_a")
    
    elif (val > 34000) and (val < 40000):
        return ('red', "upper_b")

    else:
        return ('yellow', "lower_b")

