'''
    Mark 01 - Reading wheel speeds
    
    Last update: Added wheel enconders to read the wheel speeds

    The robot can be controled in tank or arcade mode. Use the touch pad
    button to switch between.
'''
import time
import math
import pygame
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from gusbots import joystick, encoder, localization, stateControl

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

# Initialize localization
wheel_radius = 0.0335
wheel_base = 0.147

# Initialize the encoder. Both have 40 ticks per resolution.
left_wheel_encoder = encoder.encoder(5, 40, wheel_radius)
right_wheel_encoder = encoder.encoder(12, 40, wheel_radius)

odo = localization.odometry(left_wheel_encoder, right_wheel_encoder, wheel_base)
stControl = stateControl.stateControl()

last_left_dir = 1
last_right_dir = 1

x = 0
y = 0
theta = 0

# Main program loop
###################
try:
    start_time = time.time_ns()
    while True:
        left, right = joy.tick()
        left = left if left >= 0 else 0
        right = right if right >=0 else 0

        # Calculate how many ns passed since last read
        t = time.time_ns()
        dt = t - start_time
        start_time = t

        # Run odometry to update robot location
        odo.step(last_left_dir, last_right_dir)

        # Check if pose needs to be reseted by the joystick
        if (joy.resetPose == 1):
           print("Pose reseted")
           odo.resetPose()
           left_wheel_encoder.reset()
           right_wheel_encoder.reset()
        
        # Get pose values
        x, y , theta = odo.getPose()
        
        # Set inputs for the state machine
        stControl.input.joy_left = left
        stControl.input.joy_right = right
        stControl.input.autonomous = joy.autonomous
        stControl.input.x = x
        stControl.input.y = y
        stControl.input.theta = theta
        stControl.input.dt = dt
        stControl.input.el = left_wheel_encoder
        stControl.input.er = right_wheel_encoder
        stControl.input.L = wheel_base
        
        # Run state machine
        stControl.step()
        
        #print('test2', stateControl.State.output.left_motor, stateControl.State.output.right_motor)
        # Update outputs
        kit.motor1.throttle = stControl.output.left_motor
        kit.motor4.throttle = stControl.output.right_motor
        
        # The encoder can not know the direction of the motor, so we are
        # going to use the motor commands to know what direction is turning
        last_left_dir = 1 if left >=0 else -1
        last_right_dir = 1 if right >=0  else -1

        # Print some info
        #print(stateControl.State.output.left_motor, stateControl.State.output.right_motor)
        theta_d = (theta - (2 * math.pi * math.floor((theta + math.pi)/(2*math.pi))))
        theta_d = theta * 180/math.pi
        #print('Delta time', (dt/1000000), 'x', '{:02.2f}'.format(x), 'y', '{:02.2f}'.format(y), 'theta', '{:02.2f}'.format(theta_d))
        print('L/R:', left_wheel_encoder.counter, right_wheel_encoder.counter,
        'x:', '{:02.3f}'.format(x), 'y:', '{:02.3f}'.format(y), 'theta:', '{:02.2f}'.format(theta_d))

        # Limit to 10 frames per second. (100ms loop)
        clock.tick(10)
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Exiting application (clean up)
kit.motor1.throttle = 0
kit.motor4.throttle = 0
GPIO.cleanup()
pygame.quit()
