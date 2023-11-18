from pybricks.tools import wait
from hardware import Hardware
from modules.driveBase import CustomDriveBase

class Robot:
    def __init__(self):
        # Create drive base
        self._driveBase = CustomDriveBase()
        
    # Lifts a cube up, puts it in the storage and puts the lift back down
    def lift() -> None:
        # NOTE: 2950 to top without swing, 3075 entire height with swing
        # Go up
        Hardware.mediumMotor.run_angle(2500, 2920) 

        # Slow down and align cube
        Hardware.mediumMotor.run_angle(800, 12)
        Hardware.mediumMotor.run_angle(300, 8)
        Hardware.mediumMotor.run_angle(100, 100)

        # Go a bit back and swing into storage
        Hardware.mediumMotor.run_angle(2500, -120)
        Hardware.mediumMotor.run_angle(2500, 170, wait=False)
        wait(500)

        # Go back down
        Hardware.mediumMotor.run_angle(2500, -3075, wait=True)
    
    # Drops the lift and opens the back of the storage
    def openStorage():
        Hardware.mediumMotor.run_angle(1000, -720)
        Hardware.mediumMotor.run_angle(1000, 8000)