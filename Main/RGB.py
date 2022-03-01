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
    while True:
        if button.is_pressed:
            return 1    # Return 1 if button pressed then released

def StatusOn(led):
    led.color = Color('blue')

def StatusClean(led):
    led.color = Color('green')

def StatusDirty(led):
    led.color = Color('red')

def StatusMeasuring(led):
    led.color = Color('blue')
    time.sleep(0.75)
    led.color = Color('black')
    time.sleep(0.75)

def StatusSending(led):
    led.color = Color('orange')

def StatusFailSending(led):
    led.color = Color('red')
    time.sleep(0.75)
    led.color = Color('black')
    time.sleep(0.75)

def StatusOff(led):
    led.off()
