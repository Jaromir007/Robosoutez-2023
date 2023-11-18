#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

class Config:
    WHEEL_DIAMETER = 42
    AXLE_TRACK = 155

    # Driving parameters
    DRIVE_SPEED = 250
    DRIVE_ACCELERATION = 200
    TURN_RATE = 100
    TURN_ACCELERATION = 400

    # field characteristics
    TARGET_REFLECTION = 60
    LINE_REFLECTION = 8
    BRICK_DISTANCE = 280


# class RGBClassifier:

#     # Magic
#     def euclidean_distance(self, color1, color2):
#         return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5

#     def color_from_rgb(self, rgb):
#         color_ranges = {
#             "red": (16, 2, 4),
#             "green": (6, 15, 8),
#             "yellow": (22, 18, 10),
#             "white": (19, 26, 60),
#             "grey": (14, 18, 38),
#             "blue": (2, 7, 30)
#         }

#         closest_color = None
#         closest_distance = float('inf')
#         for color_name, color_range in color_ranges.items():
#             distance = self.euclidean_distance(rgb, color_range)
#             if distance < closest_distance:
#                 closest_color = color_name
#                 closest_distance = distance

#         return closest_color

# class PidLineController:

#     def __init__(self):
#         self.last_error = 0
#         self.integral = 0

#         self.PROPORTIONAL = 1.15
#         self.INTEGRAL = 0.005
#         self.DERIVATIVE = 0

#     # nevolat primo, volat z distance
#     def _follow_line(self, speed: int, side: str = "l") -> None:
#         error = color_sensor.reflection() - Config.TARGET_REFLECTION
#         p_fix = error * self.PROPORTIONAL

#         self.integral += error
#         i_fix = self.integral * self.INTEGRAL

#         derivative = self.last_error - error
#         d_fix = derivative * self.DERIVATIVE

#         self.last_error = error

#         if side == "l":
#             robot.drive(speed, -p_fix - i_fix - d_fix)

#         if side == "r":
#             robot.drive(speed, p_fix + i_fix + d_fix)

#     def distance(self, speed: int, distance: int | float, side: str = "l") -> None:
#         robot.reset()
#         while robot.distance() < distance:
#             self._follow_line(speed, side)

#         self.last_error = 0
#         self.integral = 0

class PidGyroController:
    def __init__(self):
        self.last_error = 0
        self.integral = 0

        self.PROPORTIONAL = 6
        self.DERIVATIVE = 5

    # nevolat primo, volat z distance
    def _correct_position(self, speed) -> None:
        error = gyro_sensor.angle()
        p_fix = error * self.PROPORTIONAL

        derivative = self.last_error - error
        d_fix = derivative * self.DERIVATIVE

        self.last_error = error

        robot.drive(speed, -p_fix - d_fix)
    
    def reset(self):
        self.last_error = 0
        gyro_sensor.reset_angle(0)
        robot.reset()

    def distance(self, speed: int, distance: int | float) -> None:
        self.reset()
        while robot.distance() < distance:
            self._correct_position(speed)

        robot.stop()
    
    def drive_until_black_line(self, speed: int) -> None:
        while(color_sensor.reflection() > Config.LINE_REFLECTION):
            self._correct_position(speed)
            
        robot.stop()
        left_motor.brake()
        right_motor.brake()

class CustomDriveBase(DriveBase):

    def __init__(self, left_motor, right_motor, wheel_diameter, axle_track):

        super().__init__(left_motor, right_motor, wheel_diameter, axle_track)

    #   self.line_pid = PidLineController()
        self.gyro_pid = PidGyroController()

    def gyro_turn(self, ang: int) -> None:
        initial_angle = gyro_sensor.angle()
        self.turn(ang)
        angle_diff = ang - (gyro_sensor.angle() - initial_angle)

        while abs(angle_diff) > 1:
            turn_correction = angle_diff * 0.5
            self.turn(turn_correction)
            angle_diff = ang - (gyro_sensor.angle() - initial_angle)
    
    def gyro_distance(self, distance):
        self.gyro_pid.distance(Config.DRIVE_SPEED, distance)
    
    def drive_until_black_line(self):
        self.gyro_pid.drive_until_black_line(Config.DRIVE_SPEED)
        self.straight(50)

    
    # def pid_distance(self, speed, distance, side):
    #     self.line_pid.distance(speed, distance, side)

    # def lift_cycle(self):
    #     medium_motor.run_angle(2500, 2500)
    #     wait(500)
    #     medium_motor.run_angle(2500, -2500)

    # def brick_cycle(self, repeat = 1):
    #     for i in range(repeat):
    #         self.gyro_pid.drive_until_black_line()
    #         self.lift_cycle()

    # def action(self):
    #     # prvni 4 kostky
    #     self.brick_cycle(4)
        
    #     # otocka a sebrani kostky bez cary
    #     self.gyro_distance(560)
    #     self.gyro_turn(90)
    #     self.gyro_distance(280)

    #     # druhe tri kostky 
    #     self.brick_cycle(3)

    #     # TODO dalsi kostky
            

        
        

####################### Port settings and object initialization ###################

ev3 = EV3Brick()

# Motors
left_motor = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)
right_motor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)
medium_motor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)

# Sensors
color_sensor = ColorSensor(Port.S2)
gyro_sensor = GyroSensor(Port.S1)

# New drivebase
robot = CustomDriveBase(left_motor, right_motor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)
robot.settings(Config.DRIVE_SPEED, Config.DRIVE_ACCELERATION, Config.TURN_RATE, Config.TURN_ACCELERATION)

###################################################################################

# test jak funguje pid s gyrem 

def objed_pole():
    robot.gyro_distance(1680)
    robot.gyro_turn(90)
    robot.gyro_distance(1400)
    robot.gyro_turn(90)
    robot.gyro_distance(1680)
    robot.gyro_turn(90)
    robot.gyro_distance(1400)
    robot.gyro_turn(90)

# medium_motor.run_angle(1000, -2950) # do preklopeni

def vytah():
    # POZNAMKY: 2950 do preklopeni, 3075 cely vytah
    # nahoru
    medium_motor.run_angle(2500, 2920) 

    #zpomaleni
    medium_motor.run_angle(800, 12)
    medium_motor.run_angle(300, 8)
    medium_motor.run_angle(100, 100)

    #pohyb zpatky, svih a hozeni do zasobniku
    medium_motor.run_angle(2500, -120)
    medium_motor.run_angle(2500, 170, wait=False)
    wait(500)

    # vytah uplne dolu
    medium_motor.run_angle(2500, -3075, wait=True)
    # medium_motor.run_angle(2500, -1000, wait=False)

# vypusteni kostek 
def vypustit_kostky():
    medium_motor.run_angle(1000, -720)
    medium_motor.run_angle(1000, 8000)


def vytah_loop():
    while True: 
        vytah()



# thread = threading.Thread(target=vytah_loop)
# thread.start()
# robot.straight(2500)
# thread.join()

# medium_motor.run_angle(1000, 2500, then=Stop.HOLD, wait=False)
# robot.straight(250)



# TODO Pred startem 
# zkontrolovat dvere dole 
# dat vytah na optimalni pozici
# zresetovat zachytku dveri 

# vytah()
# robot.straight(280)

# vypustit_kostky()
# ev3.speaker.beep(500, 500)


# TEST BRANI KOSTEK VE CTVERCI

def ber_kostky(kolikrat):
    for i in range(kolikrat):
        robot.drive_until_black_line()
        wait(500)
        vytah()

def kostky_ve_ctverci():
    # prvni kostka
    robot.drive_until_black_line()
    wait(500)
    vytah()

    # dalsi 3 kostky
    ber_kostky(3)
    robot.gyro_turn(90)

    ber_kostky(3)
    robot.gyro_turn(90)

    ber_kostky(4)
    robot.gyro_turn(90)

    ber_kostky(3)



kostky_ve_ctverci()
# robot.drive_until_black_line()

# while True:
#     print(color_sensor.reflection())
#     wait(500)

# podlaha 28
# bila 60
# cerna 10

