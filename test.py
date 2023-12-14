from modules.robot import Robot
from modules.hardware import Hardware
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

robot = Robot()
stopwatch = StopWatch()

# Variables ###############################

# Wall distances
wallDistance1 = 191
wallDistance2 = 326
wallDistance3 = 191
wallDistance4 = 326
# Cube properties
cubePickupSpeed = 800 # Speed when picking up cubes
cubePickupDistance = 210 # Distance to pick up a cube (usually after detecting a black line)
blackLineSpeed = 1000

# Variables end ###########################

robot.unloadStorage(500)