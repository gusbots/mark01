'''
    Mark 01 Part #4 - Odometry
'''
import time
import math
import pygame
from adafruit_motorkit import MotorKit

import RPi.GPIO as GPIO
from gusbots import joystick


# Initialize Motor HAT library
kit = MotorKit()

# Initialize pygame (used to read the joystick)
pygame.init()

# Show available joysticks in the system
# In case there are more than 1 joystick connected. Check what
# index is the one you want to use and pass to the joystick.create.
joystick.showAvailable()

# Initialize selected joystick. By default it uses TANK mode
# and index 0 for the jostick.
joy = joystick.create(joystickIndex=0, mode=joystick.TANK_MODE)

# Used to manage how fast the main loop runs
clock = pygame.time.Clock()

tick_count_left = 0
tick_count_right = 0
last_ticks_left = 0
last_ticks_right = 0
start_time = time.time_ns()

def ticksCounterLeft(pin):
    global tick_count_left
    tick_count_left += 1

def ticksCounterRight(pin):
    global tick_count_right
    tick_count_right += 1

# Setup GPIO5 to read left wheel encoder
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)
GPIO.add_event_detect(5, GPIO.BOTH, callback=ticksCounterRight)

# Setup GPIO12 to read right wheel encoder
GPIO.setup(12, GPIO.IN)
GPIO.add_event_detect(12, GPIO.BOTH, callback=ticksCounterLeft)

# Main program loop
###################
try:
    R = 0.0334          # wheels radius
    L = 0.147           # distance between the wheels
    TICKS_PER_REV = 40  # encoder ticks per revolution
    
    METERS_PER_TICK = (2*math.pi*R)/TICKS_PER_REV
    
    # Initialize pose
    x = 0
    y = 0
    theta = 0
    
    while True:
        # Read joystick inputs
        left, right = joy.tick()
        left = left if left >= 0 else 0
        right = right if right >=0 else 0

        kit.motor1.throttle = right
        kit.motor4.throttle = left

        # Calculate how many ns passed since last read
        t = time.time_ns()
        dt = t - start_time

        # Calculate the delta for ticks since last read
        delta_ticks_left = tick_count_left - last_ticks_left
        delta_ticks_right = tick_count_right - last_ticks_right

        # Update counters to next read
        last_ticks_left = tick_count_left
        last_ticks_right = tick_count_right
        start_time = t
        
        # Calculate new pose
        Dl = METERS_PER_TICK * delta_ticks_left
        Dr = METERS_PER_TICK * delta_ticks_right
        Dc = (Dr + Dl) / 2
        
        x_dt = Dc * math.cos(theta)
        y_dt = Dc * math.sin(theta)
        theta_dt = (Dr - Dl) / L
        
        x = x + x_dt
        y = y + y_dt
        theta = theta + theta_dt

        # Show data
        if (joy.resetPose == 1):
            x = 0
            y = 0
            theta = 0

        theta_d = (theta - (2 * math.pi * math.floor((theta + math.pi)/(2*math.pi)))) * 180/math.pi 
        print('Delta time', (dt/1000000), 'x', '{:02.2f}'.format(x), 'y', '{:02.2f}'.format(y), 'theta', '{:02.2f}'.format(theta_d))

        # Limit to 10 frames per second.
        clock.tick(20)
except KeyboardInterrupt:
    # Press Ctrl+C to exit the application
    pass

# Existing application (clean up)
kit.motor1.throttle  = 0
kit.motor4.throttle  = 0
GPIO.cleanup()
pygame.quit()
