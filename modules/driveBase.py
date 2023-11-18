from pybricks.robotics import DriveBase
from modules.hardware import Hardware
from config import Config
from pidGyroController import PidGyroController

class CustomDriveBase(DriveBase):

    def __init__(self):
        super().__init__(Hardware.leftMotor, Hardware.rightMotor, Config.WHEEL_DIAMETER, Config.AXLE_TRACK)

        self.gyroPid = PidGyroController()

    def gyroTurn(self, ang: int) -> None:
        initialAngle = Hardware.gyroSensor.angle()
        self.turn(ang)
        angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)

        while abs(angleDiff) > 1:
            turnCorrection = angleDiff * 0.5
            self.turn(turnCorrection)
            angleDiff = ang - (Hardware.gyroSensor.angle() - initialAngle)
    
    def gyroDistance(self, distance):
        self.gyroPid.distance(Config.DRIVE_SPEED, distance)
    
    def driveUntilBlackLine(self):
        self.gyroPid.driveUntilBlackLine(Config.DRIVE_SPEED)