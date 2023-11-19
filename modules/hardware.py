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
    leftMotor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=None)
    rightMotor = Motor(Port.B, positive_direction=Direction.CLOCKWISE, gears=None)
    mediumMotor = Motor(Port.C, positive_direction=Direction.CLOCKWISE, gears=[12, 36])

    # Sensors
    gyroSensor = GyroSensor(Port.S1)
    colorSensor = ColorSensor(Port.S2)