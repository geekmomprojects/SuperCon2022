# XIAO contains the LSM6DS3TR-C IMU with accelerometer/gyroscope
# See https://learn.adafruit.com/adafruit-lsm6ds3tr-c-6-dof-accel-gyro-imu
# for additional info
import board
import time
import digitalio
import busio
import math
import adafruit_debouncer
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC


# Make sure IMU is powered
dpwr = digitalio.DigitalInOut(board.IMU_PWR)
dpwr.direction = digitalio.Direction.OUTPUT
dpwr.value = 1
time.sleep(1)  # Seem to need this pause
i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
imu = LSM6DS3TRC(i2c)

# Computes roll and pitch from the acceration vectors.
def get_rotation_angles():
    x, y, z = imu.acceleration
    roll = math.atan2(y, z)
    pitch = math.atan2(-x, math.sqrt(y * y + z * z))
    return roll, pitch


# Returns accelerometer magnitude
def acc_magnitude():
    x, y, z = imu.acceleration
    return math.sqrt(x * x + y * y + z * z)


# Create a debouncer to detect when the IMU is shaken. Normal gravity produces a magnitude
# of 9.8 m/s^2, so we'll define "shaking" as acceleration magnitude greater than 30 m/s^2
# To learn more about using the adafruit debouncer library
# to detect sensor values above a threshold, see
# (https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/beyond-debouncing)
in_range = adafruit_debouncer.Debouncer(lambda: acc_magnitude() <= 30)

while True:
    # Uncomment the following two lines to print acceleration values. You can use
    # the Mu code editor's plotter feature to see changing values of the acceleration vectors
    ax,ay,az = imu.acceleration
    print((ax, ay, az))

    # Uncomment the following two lines to print roll and pitch angles. Roll gives you the
    # rotation angle of the IMU around the Y axis and pitch gives you the rotation of the
    # IMU about the X axis
    #roll, pitch = get_rotation_angles()
    #print((math.degrees(roll), math.degrees(pitch)))

    # Uncomment the following two lines to print the gyrsocpe values. These values
    # give you the *rate* of rotation about the Cartesian axes
    #gx, gy, gz = imu.gyro
    #print((gx, gy, gz))



    # Uncomment the following code to allow the debouncer to detect shaking
    # in_range.update()
    # if in_range.rose:  #Shake detected
    #    print("shake")

    # Rest between measurements
    time.sleep(0.1)
