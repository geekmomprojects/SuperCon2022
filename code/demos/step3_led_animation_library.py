import board
import neopixel
import imu
import adafruit_debouncer
import random

# Import the specific animation module you want. Learn more about the Adafruit
# led_animation libraries at https://learn.adafruit.com/circuitpython-led-animations
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import ORANGE, GREEN, AQUA, YELLOW

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D4

# Update to match the number of NeoPixels you have connected
pixel_num = 15

# Create a pixel object:
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.3, auto_write=False)

# Create an IMU object
imu = imu.IMU()

# Create a debouncer to detect shaking acceleration magnitude over 30 m/s^2
in_range = adafruit_debouncer.Debouncer(lambda:imu.acc_magnitude() <= 30)

# Create an object for each animation

# The rainbow animation fills all pixels with a single color that sweeps through rainbow hues
rainbow = Rainbow(pixels, speed=0.05, period=6)

# The comet animation fills all pixels with a comet in the specified color and length
comet = Comet(pixels, speed=0.04, color=(255,0,0), tail_length=4, bounce=True)

# Chase is the classic theater chase effect
chase = Chase(pixels, speed=0.05, size=3, spacing=2, color=YELLOW)

# Uncomment the line below to create an animation sequence containing all the animations
# If "advance_interval" is set to a numerical value, animations will automatically advance
# when that time interval elapses
sequence = AnimationSequence(comet, chase, rainbow, auto_clear = True, advance_interval = None)

def shake_update():
    # Update debouncer function
    in_range.update()

    # If a shake is detected, advance to the next animation
    if in_range.rose:
        print("shake")
        sequence.next()
        # Uncommenting the next line will change the color of the single color animations
        #sequence.color = random.choice([ORANGE, GREEN, AQUA, YELLOW])


while True:
    #uncomment the animation you wish to see below
    rainbow.animate()
    #comet.animate()
    #chase.animate()
    #sequence.animate()
    #shake_update()
