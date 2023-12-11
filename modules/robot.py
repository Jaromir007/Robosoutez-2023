from pybricks.parameters import Stop
from hardware import Hardware
from config import Config
from PIDDriveBase import PIDDriveBase

class Robot:
    def __init__(self):
        # Create drive base
        self.driveBase = PIDDriveBase()
        self.driveBase.settings(Config.DRIVE_SPEED, Config.DRIVE_ACCELERATION, Config.TURN_RATE, Config.TURN_ACCELERATION)

    # Movement functions

    # Sets the target wall distance for the robot
    def setWallDistance(self, distance: int) -> None:
        self.driveBase.setWallDistance(distance)

    # Driving forward (corrected)
    def driveStraight(self, speed: int, distance: int | float) -> None:
        self.driveBase.driveDistance(speed, distance)

    def driveUntilBlackLine(self, speed: int) -> None:
        while(Hardware.colorSensor.reflection() > Config.LINE_REFLECTION):
            self.driveBase.driveCorrected(speed)
            
        self.stop()
        Hardware.leftMotor.brake()
        Hardware.rightMotor.brake()

    # def driveUntilSonicDistance(self, speed: int, distance: int | float) -> None:
    #     while not Hardware.ultrasonicSensor.distance() < distance:        
    #         self.driveBase.driveCorrected(speed)
    #     self.stop()

    # Turning (not corrected)
    def turn(self, angle: int) -> None:
        self.driveBase.reset()
        self.driveBase.gyroTurn(angle)

    def oneWheelTurn(self, angle: int, motor: str) -> None:
        self.driveBase.oneWheelGyroTurn(angle, motor)

    def stop(self) -> None:
        self.driveBase.stop()
    
    # Tool functions

    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift(self) -> None:
        # Fix the lift
        Hardware.mediumMotor.run_angle(500, -30)
        Hardware.mediumMotor.run_angle(500, 30)

        Hardware.mediumMotor.run_angle(1500, 50)

        # Go up
        Hardware.mediumMotor.run_until_stalled(2500)
        # Go back down
        Hardware.mediumMotor.run_angle(2500, -870)

        # Fix the lift
        Hardware.mediumMotor.run_angle(2500, 30)
        Hardware.mediumMotor.run_angle(2500, -30)

    # Drops the lift and while opening the storage drives backwards
    def unloadStorage(self, distance: int) -> None:
        # Start driving backwards
        self.driveBase.straight(-distance)
        # Open the storage
        Hardware.mediumMotor.run_angle(2500, -1200)
        # Drive away
        self.driveBase.straight(distance)

    # Utility functions

    # Loads the lift into the robot
    def calibrateLift(self) -> None:
        Hardware.mediumMotor.run_until_stalled(2500)
        Hardware.mediumMotor.run_angle(2500, -870)

        Hardware.mediumMotor.run_angle(2500, 20)
        Hardware.mediumMotor.run_angle(2500, -20)
        Hardware.mediumMotor.run_angle(2500, 15)
        Hardware.mediumMotor.run_angle(2500, -15)

    def beep(self) -> None:
        Hardware.ev3.speaker.beep(800, 2000)
        Hardware.ev3.speaker.beep(1000, 3000)

    def waitForButton(self) -> None:
        while not Hardware.touchSensor.pressed():
            pass