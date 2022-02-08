import time
from gpiozero import RGBLED, Button
from colorzero import Color

led = RGBLED(22, 27, 17, False) # This is a common anode type RBG LED
button = Button(18, False) # The Raspi will pull up the button
while True:
    if button.is_held:
        led.color = Color('yellow')
    else:
        led.off()
    
