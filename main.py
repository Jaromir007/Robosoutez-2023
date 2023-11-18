# Import the robot class
from modules.robot import Robot

robot = Robot()

# around block
robot._driveBase.gyroDistance(1550)
robot._driveBase.gyroTurn(90)
robot._driveBase.gyroDistance(1400)
robot._driveBase.gyroTurn(90)
robot._driveBase.gyroDistance(1960)
robot._driveBase.gyroTurn(90)
robot._driveBase.gyroDistance(1400)
robot._driveBase.gyroTurn(90)