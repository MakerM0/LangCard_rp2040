# SPDX-FileCopyrightText: 2021 Ruiz Brothers for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/neopixel-ring-lamp/code

from langcard import  *
import board
import digitalio
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE



# LED_PWR = board.GP10
# # audio power,Pull SD_MODE low to place the device in shutdown
# ledpwr = digitalio.DigitalInOut(LED_PWR)
# ledpwr.direction = digitalio.Direction.OUTPUT
# ledpwr.value = False   #power on


# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 8

pixels = neopixel.NeoPixel(board.GP9, num_pixels, auto_write=True)
pixels.brightness = 0.5

rainbow = Rainbow(pixels, speed=0.01, period=1)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.05, num_sparkles=15)
rainbow_comet = RainbowComet(pixels, speed=.01, tail_length=20, bounce=True)
pulse = Pulse(pixels, speed=.05, color=PURPLE, period=3)

animations = AnimationSequence(
    pulse,
    rainbow_sparkle,
    rainbow_comet,
    rainbow,
    advance_interval=5,
    auto_clear=True,
    random_order=False
)

while True:
    animations.animate()
    key = getkey() 
    if key=='q': 
        pixels.deinit() 
        gc.collect()
        returnMainPage()
    
 
    
    