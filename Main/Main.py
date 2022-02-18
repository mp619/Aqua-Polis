from threading import Thread
from time import time
import smbus2
import TDS as TDS
import Turbidity as Turb
import RGB
import time

# Init Objects
bus = smbus2.SMBus(1)
led = RGB.RGBInit()
button = RGB.ButtonInit()

ADC_adr = 0x48 # ADC I2C address
TDS.config(bus, ADC_adr)

#Global Variable for LED Thread
STATUS = 1
# 0 Turns off thread
# 1 Clean - Green
# 2 Dirty - Red
# 3 Processing - Yellow
# 4 Sending/Receiving - Yellow Flashing

def ledcolor():
    global STATUS
    while STATUS:
        match STATUS:
            case 0:
                break   # Stop Thread
            case 1:
                RGB.StatusClean()   #Green LED
            case 2:
                RGB.StatusDirty()   #Red LED
            case 3:
                RGB.StatusMeasuring() #Yellow LED
            case 4:
                RGB.StatusSending() #Flashing LED
    RGB.StatusOff()

while True:
    STATUS = 1
    LED_Thread = Thread(target=ledcolor)
    if RGB.Press():
        STATUS = 4
        time.sleep(5)


