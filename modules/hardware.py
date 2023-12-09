# Pybricks modules
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

class Hardware:
    # Brick
    ev3 = EV3Brick()

    # Motors
    leftMotor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)
    rightMotor = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)
    mediumMotor = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)

    # Sensors
    ultrasonicSensor = UltrasonicSensor(Port.S1)
    touchSensor = TouchSensor(Port.S2)
    colorSensor = ColorSensor(Port.S3)
    gyroSensor = GyroSensor(Port.S4)