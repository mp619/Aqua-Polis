from gpiozero import RGBLED, Button
from colorzero import color

while True:
    led = RGBLED(22, 27, 17)
    led.color = Color('yellow')
