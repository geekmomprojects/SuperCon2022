# HackaDay SuperCon Workshop Example
#

"""
This example repeatedly displays all available animations, at a five second interval and
responds to input from the adafruit Bluefruit app. The left/right arrows can move the
animations forward/backwards

For NeoPixel FeatherWing. Update pixel_pin and pixel_num to match your wiring if using
a different form of NeoPixels.

This example does not work on SAMD21 (M0) boards.
"""
import board
import time
import neopixel
import digitalio
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
from imu import IMU
from tilt import Tilt
from analogio import AnalogIn  #For battery readings

color_index = 0         # Index in color_keys of the current animation color
change_interval = 1     # Seconds between color changes
next_col_time = 0       # Time to resume animation after a solid color has been displayed

autoplay = False
next_switch_time = 0    # Time to switch the animation if mode is Autoplay
play_length = 5         # Seconds for each animation in Autoplay mode


imu = IMU()

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket


from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, RED, GREEN, BLUE, YELLOW, TEAL, CYAN, BLACK, GOLD, PINK, AQUA

# Update to match the pin connected to your NeoPixels
pixel_pin1 = board.D4
# Update to match the number of NeoPixels you have connected
pixel_num = 15


pixels = neopixel.NeoPixel(pixel_pin1, pixel_num, brightness=0.2, auto_write=False)

colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
comet = Comet(pixels, speed=0.02, color=PURPLE, tail_length=4, bounce=True)
chase = Chase(pixels, speed=0.05, size=3, spacing=12, color=ORANGE)
pulse = Pulse(pixels, speed=0.03, period=3, color=BLUE)
rainbow = Rainbow(pixels, speed=0.1, period=2)
rainbow_comet = RainbowComet(pixels, speed=0.05, tail_length=6, bounce=True)
rainbow_chase = RainbowChase(pixels, speed = 0.06, size=4, spacing=6, step=30)
tilt = Tilt(pixels, imu)

color_dict = {"purple":PURPLE, "white":WHITE, "amber":AMBER, "jade":JADE, "magenta":MAGENTA, "orange":ORANGE,
              "red":RED, "green":GREEN, "blue":BLUE, "yellow":YELLOW, "teal":TEAL, "cyan":CYAN,
              "gold":GOLD, "pink":PINK, "aqua":AQUA}
color_keys = list(color_dict.keys())

anim_list = [rainbow_comet, comet, tilt, rainbow_chase, chase, pulse]
animations = AnimationSequence(
    *anim_list,
    auto_clear = True,
    advance_interval = None)

def next_animation():
    pixels.fill((0,0,0))
    animations.next()

def prev_animation():
    pixels.fill((0,0,0))
    current = animations._current
    if current > 0:
        current -= 1
    else:
        current = len(anim_list) - 1
    animations.activate(current)

def show_solid(col):
    pixels.fill(col)
    pixels.show()

def set_animation_color(col):
    animations.color = col

def goto_animation(index):
    animations.activate(index % len(anim_list))

def parse_command(s):
    print(s)
    s = s.lower()
    pos = s.find('!')
    if pos >= 0 and pos < len(s)-1:
        c = s[pos+1]
        if c == 'n':
            next_animation()
        elif c.isdigit():
            goto_animation(int(c))
    else:
        for index, k in enumerate(color_keys):
            if s.find(k) >= 0:
                color_index = index
                set_animation_color(color_dict[k])


# This function takes care of turning the animations back on if it is time to do so

def update_animations():
    global next_col_time, next_switch_time

    # If we are showing a solid color (received input from color picker), then don't
    # restart animation until the color has been displayed for the allocated time
    if animations._paused:
        if time.monotonic() > next_col_time:
            animations.resume()
    elif autoplay and time.monotonic() > next_switch_time:
        next_animation()
        next_switch_time = time.monotonic() + play_length
    animations.animate()


next_switch_time = time.monotonic() + play_length
while True:
        # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        update_animations()
    ble.stop_advertising()

    while ble.connected:
        if uart_service.in_waiting:
            try:
                packet = Packet.from_stream(uart_service)
                if isinstance(packet, ColorPacket):
                    print("color", packet.color)
                    set_animation_color(packet.color)
                    animations.freeze()
                    show_solid(packet.color)
                    next_col_time = time.monotonic() + change_interval
                    if autoplay:
                        next_switch_time += change_interval
                elif isinstance(packet, ButtonPacket):
                    if packet.button == ButtonPacket.RIGHT:
                        next_animation()
                    elif packet.button == ButtonPacket.LEFT:
                        prev_animation()
                else:
                    print("packet not recognized")
            except Exception as e:
                print(e)


        update_animations()
