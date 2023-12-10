from modules.robot import Robot
from modules.hardware import Hardware
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from modules.config import Config

from pybricks.robotics import DriveBase

robot = Robot()
stopwatch = StopWatch()

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

while True:
    robot.waitForButton()
    robot.lift()

# Wait for start button to get pressed
# while not Hardware.touchSensor.pressed():
#     print(Hardware.ultrasonicSensor.distance())

#     if Hardware.ultrasonicSensor.distance() < (wallDistance1 - 3) or Hardware.ultrasonicSensor.distance() > (wallDistance1 + 3):
#         Hardware.ev3.light.on(Color.ORANGE)
#     else:
#         Hardware.ev3.light.on(Color.GREEN)
# Hardware.ev3.light.on(Color.GREEN)

# #########################################
# Start of the sequence
# #########################################

# Reset the stopwatch
stopwatch.reset()

# ############### 1 ###############
# Pick up the first four cubes

# robot.setWallDistance(wallDistance1)

# # Pick up three cubes
# for i in range(3):
#     robot.driveUntilBlackLine(blackLineSpeed)
#     robot.lift()

# # Drive next to the next four cubes and turn
# robot.driveStraight(500, 700)
# robot.lift()
# robot.turn(-90)

# ############### 2 ###############

# robot.setWallDistance(wallDistance2)
# robot.driveUntilBlackLine(blackLineSpeed)

# for i in range(3):
#     robot.driveUntilBlackLine(blackLineSpeed)
#     robot.lift()

# Pick up the last cube
# Turn to the next wall
# robot.driveStraight(500, 380)
# robot.lift()

# # Turn to the next wall
robot.turn(-60)
robot.driveBase.straight(250)

# ############### 3 ###############

robot.setWallDistance(wallDistance3)

robot.driveUntilBlackLine(blackLineSpeed)
robot.driveStraight(50, 380)

for i in range(2):
    robot.driveUntilBlackLine(blackLineSpeed)
    robot.lift()

# Drive next to the next four cubes and turn
robot.driveStraight(500, 600)
robot.lift()
robot.turn(-90)

# ############### 4 ###############

# Update wall distance
robot.setWallDistance(wallDistance4)
robot.driveUntilBlackLine(blackLineSpeed)
robot.driveUntilBlackLine(blackLineSpeed)
robot.lift()

# ######### Release cubes #########

robot.turn(90)
robot.unloadStorage(600)

# #########################################
# End of the sequence
# #########################################

endTime = stopwatch.time()

# Make the ending sound
robot.beep()

# Calculate and show the time
duration = endTime / 1000
print(duration)
timeText = "Time:" + str(duration) + "s"
Hardware.ev3.screen.clear()
Hardware.ev3.screen.draw_text(5, 5, timeText)

# Wait for end button to get pressed
robot.waitForButton()