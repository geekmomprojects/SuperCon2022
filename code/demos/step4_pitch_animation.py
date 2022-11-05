import board
import time
import neopixel
from imu import IMU
from math import degrees
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import RAINBOW  # a list of colors in the rainbow

# Make a comet animation that changes color with the pitch (forward/back angle)
# of the headband. Could use it as a posture indicator

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D4
# Update to match the number of NeoPixels you have connected
pixel_num = 15

# Create a pixel object:
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.2, auto_write=False)
imu = IMU()

# The comet animation fills all pixels with a comet in the specified color and length
comet = Comet(pixels, speed=0.04, color=(255,0,0), tail_length=5, bounce=True)

while True:
    pitch = degrees(imu.pitch())
    index = int(abs(pitch)*len(RAINBOW)/90)
    comet.color = RAINBOW[index] # RAINBOW is just a list of colors in the rainbow
    comet.animate()
