class Config:
    WHEEL_DIAMETER = 43
    WHEEL_DISTANCE = 155

    # Driving parameters
    DRIVE_SPEED = 800
    DRIVE_ACCELERATION = 200
    TURN_RATE = 500
    TURN_ACCELERATION = 800

    # Field floor characteristics
    FLOOR_REFLECTION = 60
    LINE_REFLECTION = 20
    # Field walls characteristics
    WALL_DISTANCE1 = 190
    WALL_DISTANCE2 = 326
    WALL_DISTANCE3 = 190
    WALL_DISTANCE4 = 338

    # Cube properties
    CUBE_PICKUP_SPEED = 800 # Speed when picking up cubes
    CUBE_PICKUP_DISTANCE = 210 # Distance to pick up a cube (usually after detecting a black line)
    BLACK_LINE_SPEED = 1000