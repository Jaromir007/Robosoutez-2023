from pybricks.tools import wait
from hardware import Hardware
from config import Config
from gyroDriveBase import GyroDriveBase

class Robot:
    def __init__(self):
        # Create drive base
        self.driveBase = GyroDriveBase()
        self.driveBase.settings(Config.DRIVE_SPEED, Config.DRIVE_ACCELERATION, Config.TURN_RATE, Config.TURN_ACCELERATION)

    # Movement functions

    # Driving forward (gyro corrected)
    def driveForward(self, speed: int, distance: int | float) -> None:
        self.driveBase.driveDistance(speed, distance)

    # Turning (gyro corrected)
    def turn(self, angle: int) -> None:
        self.driveBase.turn(angle)
    
    # Tool functions

    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift(self) -> None:
        # NOTE: 2950 to top without swing, 3070 entire height with swing
        # Go up)

        # Hardware.mediumMotor.run_target(2500, 500)
        # Hardware.mediumMotor.run_target(250, 100)
        # Hardware.mediumMotor.run_target(2500, 500-40)

        Hardware.mediumMotor.run_angle(2500, 1100 - 40)
        Hardware.mediumMotor.run_angle(1000, 40)
        Hardware.mediumMotor.run_angle(1000, -40)
        Hardware.mediumMotor.run_angle(2500, -1100 + 40)

    # Drops the lift and opens the back of the storage
    def openStorage(self) -> None:
        # Throw lift
        Hardware.mediumMotor.run_angle(2500, -216)
        # Open storage
        Hardware.mediumMotor.run_angle(2500, 2520)

    # Utility functions

    # Loads the lift into the robot
    def loadLift(self) -> None:
        Hardware.mediumMotor.run_angle(2500, 141)

    def driveUntilBlackLine(self, speed):
        self.driveBase.driveUntilBlackLine(speed)