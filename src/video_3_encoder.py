'''
    Mark 01 Part #3 - Reading wheels speed
    
    This examples hows how to read the wheels encoder and convert the information
    to rpm.
    
'''
import time
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
    while True:
        # Read joystick inputs
        left, right = joy.tick()

        kit.motor1.throttle = right
        kit.motor4.throttle = left

        # Calculate how many ns passed since last read
        t = time.time_ns()
        dt = t - start_time

        # Calculate the delta for ticks since last read
        delta_ticks_left = tick_count_left - last_ticks_left
        delta_ticks_right = tick_count_right - last_ticks_right

        # Update couunters to next read
        last_ticks_left = tick_count_left
        last_ticks_right = tick_count_right
        start_time = t

        # Calculate the wheel speeds (rpm)
        rpm_left = delta_ticks_left/dt * (60/40) * 10**9
        rpm_right = delta_ticks_right/dt * (60/40) * 10**9

        # Show data
        print('Delta time', (dt/1000000), 'Left rpm', '{:02.2f}'.format(rpm_left), 'Right rpm', '{:02.2f}'.format(rpm_right))

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
