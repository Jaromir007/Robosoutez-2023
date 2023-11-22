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
    def driveStraight(self, speed: int, distance: int | float) -> None:
        self.driveBase.driveDistance(speed, distance)

    def driveUntilBlackLine(self, speed: int) -> None:
        self.driveBase.driveUntilBlackLine(speed)

    def driveUntilSonicDistance(self, speed: int, distance: int | float) -> None:
        while not Hardware.ultrasonicSensor.distance() < distance:        
            self.driveBase._correctPosition(speed)
        self.stop()

    # Turning (gyro corrected)
    def turn(self, angle: int) -> None:
        self.driveBase.gyroTurn(angle)

    def stop(self) -> None:
        self.driveBase.stop()
    
    # Tool functions

    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift(self) -> None:
        # Slowly leave the loading area
        Hardware.mediumMotor.run_angle(500, 50)
        # Go up
        Hardware.mediumMotor.run_until_stalled(1000)
        # Slowly go back
        Hardware.mediumMotor.run_angle(1000, -35)
        # Go back down
        Hardware.mediumMotor.run_angle(1000, -1147 + 35)


    # Drops the lift and opens the back of the storage
    def openStorage(self) -> None:
        # Dismount lift
        Hardware.mediumMotor.run_angle(2500, -216)
        # Open storage
        Hardware.mediumMotor.run_angle(2500, 2520)

    # Utility functions

    # Loads the lift into the robots
    def calibrateLift(self) -> None:
        Hardware.mediumMotor.run_until_stalled(250)
        Hardware.mediumMotor.run_angle(300, -1147)

    def beep(self) -> None:
        Hardware.ev3.speaker.beep(800, 200)
        Hardware.ev3.speaker.beep(1000, 300)

    def waitButton(self) -> None:
        while not Hardware.touchSensor.pressed():
            pass