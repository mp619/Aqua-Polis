from threading import Thread
import time
import smbus2
import TDS as TDS
import Turbidity as Turb
import RGB

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
        if STATUS == 0:
            break
        elif STATUS == 1:
            RGB.StatusClean(led)
        elif STATUS == 2:
            RGB.StatusDirty(led)
        elif STATUS == 3:
            RGB.StatusMeasuring(led)
        elif STATUS == 4:
            RGB.StatusSending(led)
        else:
            break
    RGB.StatusOff()

LED_Thread = Thread(target=ledcolor)
LED_Thread.start()

while True:
    if RGB.Press(button):
        STATUS = 4
        time.sleep(5)
    STATUS = 1


