from modules.hardware import Hardware
from modules.robot import Robot

robot = Robot()

while not Hardware.ultrasonicSensor.distance() < 500:
    robot.driveBase._correctPosition(250)

robot.turn(-90)

robot.driveStraight(250, 200)
    
robot.stop()