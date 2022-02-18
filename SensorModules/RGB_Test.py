import RGB
import time

led = RGB.RGBInit()
button = RGB.ButtonInit()

while True:

    RGB.StatusUnknown(led)
    if RGB.Press(button):
        RGB.StatusClean(led)
        time.sleep(5)
        RGB.StatusDirty(led)
        time.sleep(5)

