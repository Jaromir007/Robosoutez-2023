#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

class Config:
    WHEEL_DIAMETER = 56
    AXLE_TRACK = 115

    # Driving parameters
    DRIVE_SPEED = 100
    DRIVE_ACCELERATION = 200
    TURN_RATE = 100
    TURN_ACCELERATION = 400

    TARGET_REFLECTION = 60

class RGBClassifier:

    # Magic
    def euclidean_distance(self, color1, color2):
        return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

    def color_from_rgb(self, rgb):
        color_ranges = {
            "red": (16, 2, 4),
            "green": (6, 15, 8),
            "yellow": (22, 18, 10),
            "white": (19, 26, 60),
            "grey": (14, 18, 38),
            "blue": (2, 7, 30)
        }

        closest_color = None
        closest_distance = float('inf')
        for color_name, color_range in color_ranges.items():
            distance = self.euclidean_distance(rgb, color_range)
            if distance < closest_distance:
                closest_color = color_name
                closest_distance = distance

        return closest_color

class PidLineController:

    def __init__(self):
        self.last_error = 0
        self.integral = 0

        self.PROPORTIONAL = 1.15
        self.INTEGRAL = 0.005
        self.DERIVATIVE = 0

    # nevolat primo, volat z distance
    def _follow_line(self, speed: int, side: str = "l") -> None:
        error = color_sensor.reflection() - Config.TARGET_REFLECTION
        p_fix = error * self.PROPORTIONAL

        self.integral += error
        i_fix = self.integral * self.INTEGRAL

        derivative = self.last_error - error
        d_fix = derivative * self.DERIVATIVE

        self.last_error = error

        if side == "l":
            robot.drive(speed, -p_fix - i_fix - d_fix)

        if side == "r":
            robot.drive(speed, p_fix + i_fix + d_fix)

    def distance(self, speed: int, distance: int | float, side: str = "l") -> None:
        robot.reset()
        while robot.distance() < distance:
            self._follow_line(speed, side)

        self.last_error = 0
        self.integral = 0

class PidGyroController:
     def __init__(self):
        self.last_error = 0
        self.integral = 0

        self.PROPORTIONAL = 5
        self.DERIVATIVE = 5

    # nevolat primo, volat z distance
    def _correct_position(self, speed) -> None:
        error = gyro_sensor.angle()
        p_fix = error * self.PROPORTIONAL

        derivative = self.last_error - error
        d_fix = derivative * self.DERIVATIVE

        self.last_error = error

        robot.drive(speed, -p_fix - d_fix)

    def distance(self, speed: int, distance: int | float) -> None:
        gyro_sensor.reset_angle(0)
        robot.reset()
        while robot.distance() < distance:
            self._correct_position(speed)

        robot.stop()
        self.last_error = 0

class CustomDriveBase(DriveBase):

    def __init__(self, left_motor, right_motor, medium_motor, wheel_diameter, axle_track):
        super().__init__(left_motor, right_motor, wheel_diameter, axle_track)

        self.line_pid = PidLineController()
        self.gyro_pid = PidGyroController()

    def gyro_turn(self, ang: int) -> None:
        initial_angle = gyro_sensor.angle()
        self.turn(ang)
        angle_diff = ang - (gyro_sensor.angle() - initial_angle)

        while abs(angle_diff) > 1:
            turn_correction = angle_diff * 0.5
            self.turn(turn_correction)
            angle_diff = ang - (gyro_sensor.angle() - initial_angle)
    
    def gyro_distance(self, speed, distance):
        self.gyro_pid.distance(speed, distance)
    
    def pid_distance(self, speed, distance, side):
        self.line_pid.distance(speed, distance, side)

####################### Port settings and object initialization ###################

ev3 = EV3Brick()

# Motors
left_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=None)
right_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=None)
medium_motor = Motor(Port.C, positive_direction=Direction.CLOCKWISE, gears=[12, 36])

# Sensors
color_sensor = ColorSensor(Port.S1)
sonic_sensor = UltrasonicSensor(Port.S2)
gyro_sensor = GyroSensor(Port.S3)

# New drivebase
robot = CustomDriveBase(left_motor, right_motor, medium_motor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)
robot.settings(Config.DRIVE_SPEED, Config.DRIVE_ACCELERATION, Config.TURN_RATE, Config.TURN_ACCELERATION)

###################################################################################
