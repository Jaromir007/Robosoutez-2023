# Import the robot class
from modules.robot import Robot
from pybricks.tools import wait

robot = Robot()

robot.calibrateLift()

wait(100)

robot.driveForward(250, 180)
wait(50)
robot.lift()

for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveForward(250, 180)
    wait(100)
    robot.lift()

robot.driveForward(200, 280)
robot.openStorage()
robot.driveForward(150, 280)