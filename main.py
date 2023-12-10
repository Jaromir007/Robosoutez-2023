from modules.robot import Robot
from modules.hardware import Hardware
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

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
cubePickupDistance = 210 # Distance to pick up a cube (usually after detecting a black line)
blackLineSpeed = 1000

# Variables end ###########################

# Calibrate the lift
robot.calibrateLift()

# Wait for start button to get pressed
while not Hardware.touchSensor.pressed():
    print(Hardware.ultrasonicSensor.distance())

    if Hardware.ultrasonicSensor.distance() < (wallDistance1 - 3) or Hardware.ultrasonicSensor.distance() > (wallDistance1 + 3):
        Hardware.ev3.light.on(Color.ORANGE)
    else:
        Hardware.ev3.light.on(Color.GREEN)
Hardware.ev3.light.on(Color.GREEN)

# #########################################
# Start of the sequence
# #########################################

# Reset the stopwatch
stopwatch.reset()

wait(250)

# ############### 1 ###############
# Pick up the first four cubes

robot.setWallDistance(wallDistance1)
# Pick up the first cube
robot.driveStraight(cubePickupSpeed, 190)
wait(200)
robot.lift()

# Pick up the next three cubes
for i in range(3):
    robot.driveUntilBlackLine(blackLineSpeed)
    robot.driveStraight(cubePickupSpeed, cubePickupDistance)
    wait(200)
    robot.lift()

# Drive next to the next four cubes and turn
robot.driveStraight(500, 350)
robot.turn(-90)

# ############### 2 ###############

# Update wall distance
robot.setWallDistance(wallDistance2)

# Pick up three cubes
for i in range(3):
    robot.driveUntilBlackLine(blackLineSpeed)
    robot.driveStraight(cubePickupSpeed, cubePickupDistance)
    wait(200)
    robot.lift()

# Pick up the last cube
robot.driveStraight(cubePickupSpeed, 160)
robot.lift()

# Drive to the next four cubes
robot.turn(-65)
robot.driveBase.straight(240)

# ############### 3 ###############

# Update wall distance
robot.setWallDistance(wallDistance3)

# Pick up four cubes
for i in range(4):
    robot.driveUntilBlackLine(blackLineSpeed)
    robot.driveStraight(cubePickupSpeed, cubePickupDistance)
    wait(200)
    robot.lift()

# Drive next to the next four cubes and turn
robot.driveStraight(500, 380)
robot.turn(-90)

# ############### 4 ###############

# Update wall distance
robot.setWallDistance(wallDistance4)
for i in range(2):
    robot.driveUntilBlackLine(blackLineSpeed)
    robot.driveStraight(cubePickupSpeed, cubePickupDistance)
    wait(200)
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