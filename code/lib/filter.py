#implement complementary filter for a 6DOF LSM6DS3 IMU
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import time, math

class filter(LSM6DS3):
    def __init(self)__:
        self.last_read_time = 0.0
        self.last_x_angle = 0.0 #filtered angles
        self.last_y_angle = 0.0
        self.last_z_angle = 0.0
        self.last_gyro_x_angle = 0.0
        self.last_gyro_y_angle = 0.0
        self.last_gyro_z_angle = 0.0
        #calibration data to compensate for gyroscope drift
        self.base_x_gyro = 0.0
        self.base_y_gyro = 0.0
        self.base_z_gyro = 0.0

    #Generate calibration values to determine gyro drift. Hold IMU steady
    # while these measurements are taken
    def calibrate(self, nread=10, delay=0.05):
        self.base_x_gyro = 0.0
        self.base_y_gyro = 0.0
        self.base_z_gyro = 0.0
        for i in range(nread):
            self.base_x_gyro += self.gyro[0]
            self.base_y_gyro += self.gyro[1]
            self.base_z_gyro += self.gyro[2]
            time.sleep(delay)
        self.base_x_gyro /= nread
        self.base_y_gyro /= nread
        self.base_z_gyro /= nread
        last_read_time = time.monotonic()

    def compute_angles():
        # Get current readings and adjust by calibration
        gx = self.gyro[0] - self.base_x_gyro
        gy = self.gyro[1] - self.base_y_gyro
        gz = self.gyro[2] - self.base_z_gyro
        ax, ay, az = self.acceleration
        dt = time.monotonic() - last_read_time
        last_read_time = time.monotonic()
        alpha = 0.96


