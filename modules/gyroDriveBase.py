from pybricks.robotics import DriveBase
from config import Config
from hardware import Hardware

class GyroDriveBase(DriveBase):
    def __init__(self):
        super().__init__(Hardware.leftMotor, Hardware.rightMotor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)

        # Initialise variables
        self.lastError = 0
        self.integral = 0

        self.PROPORTIONAL = 6
        self.DERIVATIVE = 5

    # Turning with gyro
    def gyroTurn(self, ang: int) -> None:
        initialAngle = Hardware.gyroSensor.angle()
        self.turn(ang)
        angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)

        while abs(angleDiff) > 1:
            turnCorrection = angleDiff * 0.5
            self.turn(turnCorrection)
            angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)

        self.gyroBaseReset()

    # PID gyro driving
    def driveCorrected(self, speed) -> None:
        error = Hardware.gyroSensor.angle()
        pFix = error * self.PROPORTIONAL

        derivative = self.lastError - error
        dFix = derivative * self.DERIVATIVE

        self.lastError = error

        self.drive(speed, -pFix - dFix)
    
    def gyroBaseReset(self):
        self.lastError = 0
        Hardware.gyroSensor.reset_angle(0)
        self.reset()

    def driveDistance(self, speed: int, distance: int | float) -> None:
        startDistance = self.distance()
        while self.distance() < startDistance + distance:
            self.driveCorrected(speed)

        self.stop()