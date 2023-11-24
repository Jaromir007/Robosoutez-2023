# Import the robot class
from modules.hardware import Hardware
from modules.robot import Robot
from pybricks.tools import wait, StopWatch

stopwatch = StopWatch()
robot = Robot()

# distance after driveUntilSonicDistance function
errorToSonicDistance = 60

# distance after driveUntilBlackLine function
# distAfterBlackLine = 230 works best on original field
distAfterBlackLine = 180

# speed when picking the bricks
brickPickupSpeed = 800

# speed of the robot when looking for a black line
blackLineSpeed = 500

# Calibrate the lift
robot.calibrateLift()

# Wait for start button to get pressed
robot.waitButton()

# Start of the sequence
# Save the starting time
startTime = stopwatch.time()

# Reset the gyroDriveBase
robot.driveBase.gyroBaseReset()

wait(500)

# Pick up the first cube
robot.driveStraight(brickPickupSpeed, 180)
wait(100)
robot.lift()

# Pick up the rest of the 1st four cubes
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(brickPickupSpeed, distAfterBlackLine)
    wait(200)
    robot.lift()

# Go to the end of the field
robot.driveUntilSonicDistance(250, 500)
robot.driveStraight(250, errorToSonicDistance)

# Turn right
robot.turn(-90)


# Pick up the next four cubes
# Pick up the first three with lines beside them
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(brickPickupSpeed, distAfterBlackLine)
    wait(200)
    robot.lift()

# Pick up the last cube while going to the end of the field
robot.driveUntilSonicDistance(250, 500)
robot.driveStraight(250, errorToSonicDistance)

# Lift the 4th cube
robot.lift()

# Turn left
robot.turn(-90)


# Pick up the next two cubes
# Pick up the first three with lines beside them
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(brickPickupSpeed, 180)
    wait(200)
    robot.lift()


# Turn the back towards the center of the field
robot.turn(90)

# Back up into the center of the field
robot.driveBase.straight(-500)

# Release the cubes from storage
robot.openStorage()
# Run away from the center
robot.driveStraight(250, 250)


# End of sequence
endTime = stopwatch.time()

# Make the ending sound
robot.beep()

# Calculate and show the time
duration = (endTime - startTime) / 1000
print(duration)
timeText = "Time:" + str(duration) + "s"
Hardware.ev3.screen.clear()
Hardware.ev3.screen.draw_text(5, 5, timeText)

# Wait for end button to get pressed
robot.waitButton()