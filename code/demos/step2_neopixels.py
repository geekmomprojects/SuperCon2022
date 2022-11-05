import board
import time
import neopixel, digitalio, busio
import adafruit_debouncer

# The code to initialize the IMU and create the IMU object has been placed in
# the file ../lib/imu.py, so we can import it as a module
import imu

# Create IMU object
imu = imu.IMU()

# Update to match the pin connected to your NeoPixels
pixel_pin = board.D4

# Update to match the number of NeoPixels you have connected
pixel_num = 15

# Create a neopixel object. Keeping the brightness lower reduces power consumption, but
# gives a smaller range of visible color values
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.3, auto_write=False)

# neopixel colors are defined as an RGB tuple, so (255,0,0) is Red
#pixels.fill((255,0,0))

# changes aren't visible until "show" is called (unless auto_write is True)
#pixels.show()

# Uncomment the lines below to change the color of the specified pixel
#time.sleep(1)
#pixels.fill((0,0,0))        #Fill with Black
#pixels[5] = (0, 255, 0)     #Set pixel #6 Green
#pixels.show()

# To learn more about using the adafruit debouncer library to detect sensor values above a threshold, see
#(https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/beyond-debouncing)
in_range = adafruit_debouncer.Debouncer(lambda:imu.acc_magnitude() <= 30)

cur_pixel = 0
def show_next_pixel(color = (255,0,0)):
    global cur_pixel
    pixels[cur_pixel] = (0,0,0)
    cur_pixel = (cur_pixel + 1) % pixel_num
    pixels[cur_pixel] = color
    pixels.show()

# Fill the pixels with a flash of color for 1/4 second
def color_flash(color = (0,0,255)):
    pixels.fill(color)
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0,0,0))
    pixels.show()

last_advance_time = 0
while True:
    # The code below shows an animated pixel moving down the strip every 1/2 second
    # It is written to be non-blocking. Instead of pausing execution for 1/2 second
    # it continuously checks for the next time to advance the pixel, so other code
    # can run in the meantime.
    if time.monotonic() - last_advance_time > 0.5:
        show_next_pixel()
        last_advance_time = time.monotonic()

    #Uncomment the code below to flash all pixels blue when the imu detects shaking
    in_range.update()
    if in_range.rose:  #Shake detected
        show_flash()
