'''
    Mark 01 - Driving the DC motors with PS4 controller in tank mode
    
    This first version of the robot software will drive the 2 DC motors using a PS4 controller.
    The joystick interface is tank mode where each stick of the joystick commands a different motor.
    
'''
import pygame
from adafruit_motorkit import MotorKit

# Initialize Motor HAT library
kit = MotorKit()

# Initialize pygame (used to read the joystick)
pygame.init()

# Global variables
done = False            # when True, program will end
useJoystick = 0         # select what joystick index to use

# Used to manage how fast the main loop runs
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get count of joysticks.
joystick_count = pygame.joystick.get_count()
print("Joystick count:" + str(joystick_count))

# Show all available joysticks
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    # Get the name from the OS for the controller/joystick.
    name = joystick.get_name()
    print("Joystick name:" + name)

    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    print("Number of axes:" + str(axes))

# Setup what joystick to use
joystick = pygame.joystick.Joystick(useJoystick)
joystick.init()
axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()


# Main program loop
###################
while not done:
    for event in pygame.event.get(): # User did something.
        pass
            
    for i in range(axes):
        axis = joystick.get_axis(i)
        # Left stick up/down (right wheel)
        if i == 1:
            if axis < 0.3 and axis > -0.3:
                axis = 0
            kit.motor1.throttle = axis
            print("Motor 1:", axis)

        # Right stick up/down (left wheel)
        if i == 5:
            if axis < 0.3 and axis > -0.3:
                axis = 0
            kit.motor4.throttle = axis
            print("Motor 4:", axis)

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()