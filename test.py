from modules.robot import Robot
from modules.hardware import Hardware
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from modules.config import Config

from pybricks.robotics import DriveBase

robot = Robot()
# stopwatch = StopWatch()

# Variables ###############################

# Wall distances
wallDistance1 = 67
wallDistance2 = 190
wallDistance3 = 67
wallDistance4 = 190
# Cube properties
cubePickupSpeed = 800 # Speed when picking up cubes
cubePickupDistance = 200 # Distance to pick up a cube (usually after detecting a black line)
blackLineSpeed = 1000

# # Variables end ###########################

robot.calibrateLift()

for i in range(3):
    robot.driveUntilBlackLine(500)
    robot.lift()