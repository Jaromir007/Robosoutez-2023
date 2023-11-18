from config import Config
from hardware import Hardware

class PidGyroController:
    def __init__(self, driveBase, gyroSensor):
        self.driveBase = driveBase
        self.gyroSensor = gyroSensor

        # Initialise variables
        self.lastError = 0
        self.integral = 0

        self.PROPORTIONAL = 6
        self.DERIVATIVE = 5

    def _correctPosition(self, speed) -> None:
        error = self.gyroSensor.angle()
        pFix = error * self.PROPORTIONAL

        derivative = self.lastError - error
        dFix = derivative * self.DERIVATIVE

        self.lastError = error

        self.driveBase.drive(speed, -pFix - dFix)
    
    def reset(self):
        self.lastError = 0
        self.gyroSensor.reset_angle(0)
        self.driveBase.reset()

    def distance(self, speed: int, distance: int | float) -> None:
        self.reset()
        while self.driveBase.distance() < distance:
            self._correctPosition(speed)

        self.driveBase.stop()
    
    def driveUntilBlackLine(self, speed: int) -> None:
        while(Hardware.colorSensor.reflection() > Config.LINE_REFLECTION):
            self._correctPosition(speed)
            self.driveBase.straight()
            
        self.driveBase.stop()
        self.driveBase.leftMotor.brake()
        self.driveBase.rightMotor.brake()