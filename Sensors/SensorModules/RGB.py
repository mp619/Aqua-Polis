import time
from gpiozero import RGBLED, Button
from colorzero import Color

RED_PIN = 22
GREEN_PIN = 27
BLUE_PIN = 17
BUTTON_PIN = 18

def RGBInit():
    led = RGBLED(RED_PIN, GREEN_PIN, BLUE_PIN, False) # This is a common anode type RBG LED
    return led
    
def ButtonInit():
    button = Button(BUTTON_PIN, False)  # The Raspi will pull up the button
    return button

def Press(button):    # Return a bool if button is pressed and let go
    if button.is_pressed:
        if not button.is_pressed:
            return 1    # Return 1 if button pressed then released
    return 0    # Return 0 if button not released

def StatusClean(led):
    led.color = Color('Green')

def StatusDirty(led):
    led.color = Color('Red')

def StatusUnknown(led):
    led.blink(1,1,0.25,0.25,Color('Yellow'), (0,0,0))