from modules.robot import Robot
from modules.hardware import Hardware
from modules.config import Config
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

robot = Robot()
stopwatch = StopWatch()

# Calibrate the lift
robot.calibrateLift()

# Wait for start button to get pressed
while not Hardware.touchSensor.pressed():
    # print(Hardware.ultrasonicSensor.distance())

    if Hardware.ultrasonicSensor.distance() < (Config.WALL_DISTANCE1 - 3) or Hardware.ultrasonicSensor.distance() > (Config.WALL_DISTANCE1 + 3):
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

robot.setWallDistance(Config.WALL_DISTANCE1)
# Pick up the first cube
robot.driveStraight(Config.CUBE_PICKUP_SPEED, 190)
wait(200)
robot.lift()

# Pick up the next two cubes
for i in range(2):
    robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
    robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
    wait(200)
    robot.lift()

# Pick up the last cube
robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
wait(200)
robot.shakeLift()

# Drive next to the next four cubes and turn
robot.driveStraight(500, 290)
robot.oneWheelTurn(-90, "right")
robot.lift()

# ############### 2 ###############

# Update wall distance
robot.setWallDistance(Config.WALL_DISTANCE2)

# Pick up three cubes
for i in range(3):
    robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
    robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
    wait(200)
    robot.lift()

# Pick up the last cube
robot.driveStraight(Config.CUBE_PICKUP_SPEED, 150)
robot.shakeLift()

# Drive to the next four cubes
robot.oneWheelTurn(-90, "right")
robot.lift()

# ############### 3 ###############

# Update wall distance
robot.setWallDistance(Config.WALL_DISTANCE3)

# Pick up four cubes
for i in range(3):
    robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
    robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
    wait(200)
    robot.lift()

# Drive next to the next four cubes and turn
robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
wait(200)
robot.driveStraight(500, 330)
robot.oneWheelTurn(-90, "right")
robot.lift()

# ############### 4 ###############

# Update wall distance
robot.setWallDistance(Config.WALL_DISTANCE4)
robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
robot.driveStraight(Config.CUBE_PICKUP_SPEED, Config.CUBE_PICKUP_DISTANCE)
wait(200)
robot.lift()

robot.driveUntilBlackLine(Config.BLACK_LINE_SPEED)
robot.driveStraight(Config.CUBE_PICKUP_SPEED, 230)
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