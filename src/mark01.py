'''
    Mark 01 - Reading wheel speeds
    
    Last update: Added wheel enconders to read the wheel speeds

    The robot can be controled in tank or arcade mode. Use the touch pad
    button to switch between.
'''
import time
import pygame
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from gusbots import joystick, encoder, speedEstimator

# Initialize Motor HAT library
kit = MotorKit()

# Show available joysticks in the system
# In case there are more than 1 joystick connected. Check what
# index is the one you want to use and pass to the joystick.create.
joystick.showAvailable()

# Initialize selected joystick. By default it uses ARCADE mode
# and index 0 for the jostick.
joy = joystick.create(joystickIndex=0, mode=joystick.ARCADE_MODE)

# Used to manage how fast the main loop runs
clock = pygame.time.Clock()

# Initialize the encoder. Both have 40 ticks per resolution.
left_wheel_encoder = encoder.encoder(5, 40)
right_wheel_encoder = encoder.encoder(12, 40)

# Initialize the speed estimator
wheel_radius = 0.030988
wheel_base = 0.141478
speed = speedEstimator.speedEstimator(left_wheel_encoder, right_wheel_encoder, wheel_radius, wheel_base)

# Main program loop
###################
try:
    start_time = time.time_ns()
    while True:
        left, right = joy.tick()

        kit.motor1.throttle = left
        kit.motor4.throttle = right

        # Calculate how many ns passed since last read
        t = time.time_ns()
        dt = t - start_time
        start_time = t

        # The encoder can not know the direction of the motor, so we are
        # going to use the motor commands to know what direction is turning
        dir_left = 1 if left >=0 else -1
        dir_right = 1 if right >=0  else -1

        # Get wheel speeds (call every loop - dt can not be big)
        left_wheel_speed, right_wheel_speed = speed.wheelSpeed(dt, dir_left, dir_right)
        robot_v, robot_w = speed.robotSpeed(left_wheel_speed, right_wheel_speed)

        # Print some info always in the same line
        print('Delta time', '{:05.1f}'.format(dt/1000000), 'Left:', '{:06.2f}'.format(left_wheel_speed), 'rpm Right:', '{:06.2f}'.format(right_wheel_speed), 'rpm Robot: v', '{:06.2f}'.format(robot_v*100), 'cm/s, w', '{:06.2f}'.format(robot_w*57.2958), 'deg/s')
        
        # Limit to 10 frames per second. (100ms loop)
        clock.tick(10)
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Existing application (clean up)
kit.motor1.throttle = 0
kit.motor4.throttle = 0
GPIO.cleanup()
pygame.quit()
