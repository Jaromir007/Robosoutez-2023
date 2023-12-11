from modules.robot import Robot
from modules.hardware import Hardware
from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch

robot = Robot()
stopwatch = StopWatch()

# Variables ###############################

# Wall distances
wallDistance1 = 72
wallDistance2 = 210
wallDistance3 = 72
wallDistance4 = 210
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