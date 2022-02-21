import RGB
import time

led = RGB.RGBInit()
button = RGB.ButtonInit()

while True:
    RGB.StatusUnknown()
    if RGB.Button(button):
        RGB.StatusClean
        time.sleep(5)
        RGB.StatusDirty
        time.sleep(5)

