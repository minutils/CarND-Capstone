from pid import PID
from lowpass import LowPassFilter
from yaw_controller import YawController
import math
import matplotlib.pyplot as plt

GAS_DENSITY = 2.858
ONE_MPH = 0.44704

class Controller(object):
    def __init__(self, vehicle_mass, fuel_capacity, brake_deadband, decel_limit, accel_limit, wheel_radius,
                 wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
        self.pid = PID(5., 0.1, 1.)
        self.yaw = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)
        self.filter = LowPassFilter(0.5, 1. / 50.)

        self.vehicle_mass = vehicle_mass
        self.fuel_capacity = fuel_capacity
        self.brake_deadband = brake_deadband
        self.decel_limit = decel_limit
        self.accel_limit = accel_limit
        self.wheel_radius = wheel_radius
        self.max_throttle = 1.

    def control(self, target_linear, target_angular, current_linear, step):
        throttle = 0.
        brake = 0.
        value = self.pid.step(target_linear - current_linear, step)
        if value > 0.:
            value = min(self.accel_limit, value)
            throttle = min(self.max_throttle, value)
            throttle = self.filter.filt(throttle)
        else:
            value = max(self.decel_limit, value)
            mass = self.vehicle_mass + GAS_DENSITY * self.fuel_capacity
            brake = self.filter.filt(-value * mass * self.wheel_radius)
            if brake < self.brake_deadband:
                brake = 0.
        steer = self.yaw.get_steering(target_linear, target_angular, current_linear)

        return throttle, brake, steer
