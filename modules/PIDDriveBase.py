from pybricks.parameters import Number, Stop
from pybricks.robotics import DriveBase
from config import Config
from hardware import Hardware

class PIDDriveBase(DriveBase):
    def __init__(self):
        super().__init__(Hardware.leftMotor, Hardware.rightMotor, Config.WHEEL_DIAMETER, Config.WHEEL_DISTANCE)

        # Initialise constants
        self.PROPORTIONAL = 2
        self.DERIVATIVE = 2

        # Initialise variables
        self.lastError = 0
        self.targetWallDistance = 100

    def setWallDistance(self, distance: int) -> None:
        self.targetWallDistance = distance

    def reset(self) -> None:
        self.lastError = 0
        Hardware.gyroSensor.reset_angle(0)
        super().reset()

    # Turning function inherited from DriveBase

    # PID driving
    def driveCorrected(self, speed: int) -> None:
        sonicDistance = Hardware.ultrasonicSensor.distance()

        error = sonicDistance - self.targetWallDistance
        pFix = error * self.PROPORTIONAL

        derivative = self.lastError - error
        dFix = derivative * self.DERIVATIVE

        self.lastError = error

        self.drive(speed, pFix + dFix)

    def driveDistance(self, speed: int, distance: int | float) -> None:
        startDistance = self.distance()
        while self.distance() < startDistance + distance:
            self.driveCorrected(speed)

        self.stop()

    # Gyro turning
    def gyroTurn(self, angle: int) -> None:
        Hardware.gyroSensor.reset_angle(0)

        # Python doesn't have sign function
        if (angle > 0):
            Hardware.leftMotor.run(600)
            Hardware.rightMotor.run(-600)
        else:
            Hardware.leftMotor.run(-600)
            Hardware.rightMotor.run(600)

        while abs(Hardware.gyroSensor.angle()) < abs(angle) - 5:
            pass

        Hardware.leftMotor.brake()
        Hardware.rightMotor.brake()

    # def oneWheelGyroTurn(self, angle: int, motor: str) -> None:
    #     Hardware.gyroSensor.reset_angle(0)

    #     sign = 1
    #     if (angle < 0):
    #         sign = -1

    #     if (motor == "left"):
    #         Hardware.leftMotor.run(600 * sign)
    #     else:
    #         Hardware.rightMotor.run(600 * -sign)

    #     while abs(Hardware.gyroSensor.angle()) < abs(angle):
    #         pass

    #     Hardware.leftMotor.brake()
    #     Hardware.rightMotor.brake()


#  je to nechutny, zabere to cas, ale s nicim lepsim jsem neprisel, musite to prepsat 
# kazdopadne to funguje a s nicim dalsim uz jsem problemy nemel, podivejte se na to co jsem napsal do statistik
    def oneWheelGyroTurn(self, angle: int, motor: str) -> None:
        Hardware.gyroSensor.reset_angle(0)

        sign = 1
        if (angle < 0):
            sign = -1

        if (motor == "left"):
            while abs(Hardware.gyroSensor.angle()) < abs(angle)-5:
                Hardware.leftMotor.run(600 * sign)
                Hardware.rightMotor.hold()
            Hardware.leftMotor.brake()

        else:
            while abs(Hardware.gyroSensor.angle()) < abs(angle)-5:
                Hardware.rightMotor.run(600 * -sign)
                Hardware.leftMotor.hold()
            Hardware.rightMotor.brake()

