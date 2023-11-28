from pybricks.robotics import DriveBase
from config import Config
from hardware import Hardware

class PIDDriveBase(DriveBase):
    def __init__(self):
        super().__init__(Hardware.leftMotor, Hardware.rightMotor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)

        # Initialise variables
        self.lastError = 0
        self.integral = 0

        self.PROPORTIONAL = 6
        self.DERIVATIVE = 5

        self.targetWallDistance = 50

    def setWallDistance(self, distance: int) -> None:
        self.targetWallDistance = distance

    def reset(self) -> None:
        self.lastError = 0
        super().reset()

    # Turning function inherited from DriveBase

    # PID driving
    def driveCorrected(self, speed: int) -> None:
        error = Hardware.ultrasonicSensor.distance() - self.targetWallDistance
        pFix = error * self.PROPORTIONAL

        derivative = self.lastError - error
        dFix = derivative * self.DERIVATIVE

        self.lastError = error

        self.drive(speed, -pFix - dFix)

    def driveDistance(self, speed: int, distance: int | float) -> None:
        startDistance = self.distance()
        while self.distance() < startDistance + distance:
            self.driveCorrected(speed)

        self.stop()