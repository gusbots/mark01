'''
    Mark 01 - Driving the DC motors with PS4 controller in arcade mode
    
    Now you can control the robot in tank or arcade mode. Use the touch pad
    button to switch between.
    
'''
import pygame
from adafruit_motorkit import MotorKit
from gusbots import joystick

# Initialize Motor HAT library
kit = MotorKit()

# Initialize pygame (used to read the joystick)
pygame.init()

# Show available joysticks in the system
# In case there are more than 1 joystick connected. Check what
# index is the one you want to use and pass to the joystick.create.
joystick.showAvailable()

# Initialize selected joystick. By default it uses ARCADE mode
# and index 0 for the jostick.
joy = joystick.create(joystickIndex=0, mode=joystick.ARCADE_MODE)

# Global variables
done = False            # when True, program will end
useJoystick = 0         # select what joystick index to use

# Used to manage how fast the main loop runs
clock = pygame.time.Clock()


# Main program loop
###################
while not done:
    left, right = joy.tick()
             
    kit.motor1.throttle = left
    kit.motor4.throttle = right
    
    # Print some info always in the same line
    print("\r", "Mode", joy.mode, "Left Motor (1)", '{:02.2f}'.format(left), "Right Motor (4)", '{:02.2f}'.format(right),"  ", end='')
    
    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()