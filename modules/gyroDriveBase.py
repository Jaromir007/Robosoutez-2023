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