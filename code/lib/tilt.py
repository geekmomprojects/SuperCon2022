from adafruit_led_animation.animation import Animation
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import board, time, digitalio, busio
from imu import IMU
from math import atan2, sqrt, degrees
import random

DEGREES_PER_PIXEL = 200/15 # 15 pixels spread over approximately 200 degrees of arc

# Constrains a value n to a min/max range
def clamp(n, mn, mx):
    return min(max(n,mn),mx)


class Tilt(Animation):
    """
    Tilt Animation
    :param pixel_object: The initialised LED object.
    :param imu: object of class IMU
    :param speed: time between refreshes
    """


    def __init__(
        self,
        pixel_object,  # This is the neopixel object we passed in
        imu,
        speed=.05,
        color = (0,255,0),
        name=None
    ):
        super().__init__(pixel_object, speed, color=color, name=name)
        self.imu = imu
        self.reset()
        # When the headband is held upright, the orientation of the XIAO board
        # is approximately -120 degrees (close enough for our purposes, anyway)
        self.center = -120


    def reset(self):
        self.pixel_object.fill((0,0,0))

    # Base color on pitch, position on roll
    def draw(self):
        roll = degrees(self.imu.roll())
        #print(roll)
        # npix is the number of pixels in the strip
        npix = self.pixel_object.n  #number of pixels in the strip
        middle = npix/2
        # Headband covers about 200 degrees of a circle with 15 pixels
        # Dist is how far away from center we are in pixels
        dist = (self.center-roll)/DEGREES_PER_PIXEL
        # Keep the displayed pixel between 0 and the length of the strip
        pix = clamp(int(round(middle + dist)),0,npix - 1)
        # Clear any old pixels
        self.pixel_object.fill((0,0,0))
        self.pixel_object[pix] = self.color
