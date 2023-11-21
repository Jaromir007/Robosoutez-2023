from modules.hardware import Hardware
from modules.robot import Robot
from pybricks.tools import wait

robot = Robot()

robot.beep()

robot.calibrateLift()

while True:
    robot.waitButton()
    robot.driveBase.gyroBaseReset()
    robot.driveStraight(250, 150)
    robot.lift()
    robot.driveBase.straight(-220)
