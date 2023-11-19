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
    def driveForward(self, distance: int | float) -> None:
        self.driveBase.driveDistance(Config.DRIVE_SPEED, distance)

    # Turning (gyro corrected)
    def turn(self, angle: int) -> None:
        self.driveBase.turn(angle)
    
    # Tool functions

    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift(self) -> None:
        # NOTE: 2950 to top without swing, 3070 entire height with swing
        # Go up
        Hardware.mediumMotor.run_angle(2500, (3070 - 135))
        # Align the cube
        Hardware.mediumMotor.run_angle(250, 70)
        # Go back a bit
        Hardware.mediumMotor.run_angle(2500, -60)
        # Swing the cube into storage
        Hardware.mediumMotor.run_angle(2500, 135-70+60)
        # Go back down
        Hardware.mediumMotor.run_angle(2500, -3070)

    # Drops the lift and opens the back of the storage
    def openStorage(self) -> None:
        # Throw lift
        Hardware.mediumMotor.run_angle(2500, -600)
        # Open storage
        Hardware.mediumMotor.run_angle(2500, 7000)

    # Utility functions

    # Loads the lift into the robot
    def loadLift(self) -> None:
        Hardware.mediumMotor.run_angle(2500, 390)