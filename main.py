# Import the robot class
from modules.hardware import Hardware
from modules.robot import Robot
from pybricks.tools import wait, StopWatch

stopwatch = StopWatch()
robot = Robot()

# Calibrate the lift
robot.calibrateLift()

# Testing code start

exit()
# Testing code end

# Wait for start button to get pressed
while not Hardware.touchSensor.pressed():
    pass

# Start of the sequence
startTime = stopwatch.time()

# Restart the gyroDriveBase
robot.driveBase.gyroBaseReset()

wait(500)

# Pick up the first cube
robot.driveStraight(250, 180)
wait(100)
robot.lift()

# Pick up the rest of the 1st four cubes
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(250, 180)
    wait(200)
    robot.lift()

# Go to the end of the field
robot.driveStraight(250, 1540 - robot.driveBase.distance())

# Turn right
robot.turn(-90)

# Pick up the next four cubes
# Pick up the first three with lines beside them
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(250, 180)
    wait(200)
    robot.lift()

# Pick up the last cube while going to the end of the field
robot.driveStraight(250, 1370 - robot.driveBase.distance())
# Lift the 4th cube
robot.lift()

# Turn left
robot.turn(-90)

# Pick up the next four cubes
# Pick up the first three with lines beside them
for i in range(4):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(250, 180)
    wait(200)
    robot.lift()

# Go to the end of the field
robot.driveStraight(250, 1870 - robot.driveBase.distance())

# Turn left
robot.turn(-90)

# Pick up the next four cubes
# Pick up the first three with lines beside them
for i in range(3):
    robot.driveUntilBlackLine(140)
    robot.driveStraight(250, 180)
    wait(200)
    robot.lift()

# Pick up the last cube while going to the end of the field
robot.driveStraight(250, 1370 - robot.driveBase.distance())
# Lift the 4th cube
robot.lift()

# Turn the back towards the center of the field
robot.turn(45)
# Back up into the center of the field
robot.driveStraight(250, -1000)

# Release the cubes from storage
robot.openStorage()
# Run away from the center
robot.driveStraight(150, 1000)

# End of sequence
endTime = stopwatch.time()
robot.beep()

# Calculate and show the time
duration = (endTime - startTime) / 1000
print(duration)
timeText = "Time:" + str(duration) + "s"
Hardware.ev3.screen.clear()
Hardware.ev3.screen.draw_text(5, 5, timeText)

while not Hardware.touchSensor.pressed():
    pass