#Create our own custom LED animation to use the accelerometer
import board, time, neopixel
from imu import IMU
from tilt import Tilt

# Update to match the pin connected to your NeoPixels
pixel_pin1 = board.D4
# Update to match the number of NeoPixels you have connected
pixel_num = 15


pixels = neopixel.NeoPixel(pixel_pin1, pixel_num, brightness=0.2, auto_write=False)
imu = IMU()

# The tilt animation moves a single pixel around the headband so that it stays
# near the top fo the band as it rotates. It reacts to the side to side tilt (roll angle)
# See tilt.py in the lib directory for the code
tilt = Tilt(pixels, imu)

while True:
    tilt.animate()
