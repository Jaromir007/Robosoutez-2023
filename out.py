#!/usr/bin/env pybricks-micropython
# Auto generated file
# Pybricks modules 
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor) 
from pybricks.parameters import Port, Stop, Direction, Button, Color 
from pybricks.tools import wait, StopWatch, DataLog 
from pybricks.robotics import DriveBase 
from pybricks.media.ev3dev import SoundFile, ImageFile

#===========================================
#/Users/honzakubita/programming/Robosoutez/modules/config.py
#===========================================
class Config:
    WHEEL_DIAMETER = 42
    AXLE_TRACK = 155

    # Driving parameters
    DRIVE_SPEED = 250
    DRIVE_ACCELERATION = 200
    TURN_RATE = 100
    TURN_ACCELERATION = 400

    # field characteristics
    FLOOR_REFLECTION = 60
    LINE_REFLECTION = 8
    BRICK_DISTANCE = 280
#===========================================
#/Users/honzakubita/programming/Robosoutez/modules/hardware.py
#===========================================
# Pybricks modules

class Hardware:
    # Brick
    ev3 = EV3Brick()

    # Motors
    leftMotor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=None)
    rightMotor = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=None)
    mediumMotor = Motor(Port.C, positive_direction=Direction.CLOCKWISE, gears=[12, 36])

    # Sensors
    gyroSensor = GyroSensor(Port.S1)
    colorSensor = ColorSensor(Port.S2)
#===========================================
#/Users/honzakubita/programming/Robosoutez/modules/gyroDriveBase.py
#===========================================

class GyroDriveBase(DriveBase):
    def __init__(self):
        super().__init__(Hardware.leftMotor, Hardware.rightMotor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)

        # Initialise variables
        self.lastError = 0
        self.integral = 0

        self.PROPORTIONAL = 6
        self.DERIVATIVE = 5

    # Turning with gyro
    def turn(self, ang: int) -> None:
        initialAngle = Hardware.gyroSensor.angle()
        self.turn(ang)
        angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)

        while abs(angleDiff) > 1:
            turnCorrection = angleDiff * 0.5
            self.turn(turnCorrection)
            angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)

    # PID gyro driving
    def _correctPosition(self, speed) -> None:
        error = Hardware.gyroSensor.angle()
        pFix = error * self.PROPORTIONAL

        derivative = self.lastError - error
        dFix = derivative * self.DERIVATIVE

        self.lastError = error

        self.drive(speed, -pFix - dFix)
    
    def reset(self):
        self.lastError = 0
        Hardware.gyroSensor.reset_angle(0)
        self.reset()

    def driveDistance(self, speed: int, distance: int | float) -> None:
        self.reset()
        while self.distance() < distance:
            self._correctPosition(speed)

        self.stop()
    
    def driveUntilBlackLine(self, speed: int) -> None:
        while(Hardware.colorSensor.reflection() > Config.LINE_REFLECTION):
            self._correctPosition(speed)
            self.straight()
            
        self.stop()
        Hardware.leftMotor.brake()
        Hardware.rightMotor.brake()
#===========================================
#/Users/honzakubita/programming/Robosoutez/modules/robot.py
#===========================================

class Robot:
    def __init__(self):
        # Create drive base
        self.driveBase = GyroDriveBase()
        self.driveBase.settings(Config.DRIVE_SPEED, Config.DRIVE_ACCELERATION, Config.TURN_RATE, Config.TURN_ACCELERATION)

    def driveForward(self, speed: int, distance: int | float) -> None:
        self.driveBase.driveDistance(speed, distance)
        
    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift(self) -> None:
        # NOTE: 2950 to top without swing, 3075 entire height with swing
        # Go up
        Hardware.mediumMotor.run_angle(2500, 2920) 

        # Slow down and align cube
        Hardware.mediumMotor.run_angle(800, 12)
        Hardware.mediumMotor.run_angle(300, 8)
        Hardware.mediumMotor.run_angle(100, 100)

        # Go a bit back and swing into storage
        Hardware.mediumMotor.run_angle(2500, -120)
        Hardware.mediumMotor.run_angle(2500, 170, wait=False)
        wait(500)

        # Go back down
        Hardware.mediumMotor.run_angle(2500, -3075, wait=True)
    
    # Drops the lift and opens the back of the storage
    def openStorage(self) -> None:
        Hardware.mediumMotor.run_angle(1000, -720)
        Hardware.mediumMotor.run_angle(1000, 8000)
#===========================================
#/Users/honzakubita/programming/Robosoutez/main.py
#===========================================
# Import the robot class

robot = Robot()

robot.driveForward(300, 500)