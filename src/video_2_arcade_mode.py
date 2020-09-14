'''
    Mark 01 - Driving the DC motors with PS4 controller in arcade
    
    This example shows how to control the robot using the R2 to go foward, the L2
    to go backwards and the left stick to make turns.
    
'''
import pygame
from adafruit_motorkit import MotorKit

# Initialize Motor HAT library
kit = MotorKit()

# Initialize pygame (used to read the joystick)
pygame.init()

# Global variables
done = False                # when True, program will end
useJoystick = 0             # select what joystick index to use
R2NeverPressed = True       # Turns to false after first time R2 is pressed
L2NeverPressed = True       # Turns to false after first time L2 is pressed

# Used to manage how fast the main loop runs
clock = pygame.time.Clock()

# Initialize the joysticks
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


# Main program loop
###################
while not done:
    #
    # EVENT PROCESSING STEP
    #
    # Keep this code even if not used.
    for event in pygame.event.get():
        pass

    # Reset motor commands before reading new joystick inputs
    motor1 = 0
    motor4 = 0
    
    for i in range(axes):
        axis = joystick.get_axis(i)
        # R2
        # When never pressed R2 has a value of 0. After the first use, when released,
        # R2 has a value of -1. When full pressed it has a value of 1.
        if i == 3:
            # Check if pressed for the first time
            if R2NeverPressed == True and axis != 0:
                R2NeverPressed = False
            
            if R2NeverPressed == False:
                if axis < 0.3 and axis > -0.3:
                    axis = 0

                motor1 = motor1 + (axis + 1)/2
                motor4 = motor4 + (axis + 1)/2

        # L2
        # When never pressed L2 has a value of 0. After the first use, when released,
        # L2 has a value of -1. When full pressed it has a value of 1.
        if i == 4:
            # Check if pressed for the first time
            if L2NeverPressed == True and axis != 0:
                L2NeverPressed = False
            
            if L2NeverPressed == False:
                if axis < 0.3 and axis > -0.3:
                    axis = 0

                motor1 = motor1 - (axis + 1)/2
                motor4 = motor4 - (axis + 1)/2

        # Left stick left/right
        if i == 0:
            if axis < 0.3 and axis > -0.3:
                axis = 0
        
            if motor1 >= 0:
                motor1 = motor1 - axis
            else:
                motor1 = motor1 + axis
                
            if motor4 >=0:
                motor4 = motor4 + axis
            else:
                motor4 = motor4 - axis   

        # Limit the output between -1 and 1
        if motor1 > 1:
            motor1 = 1
        
        if motor4 > 1:
            motor4 = 1
            
        if motor1 < -1:
            motor1 = -1
        
        if motor4 < -1:
            motor4 = -1
    
    # Assign motor commands to the motors
    kit.motor1.throttle = motor1
    kit.motor4.throttle = motor4
    print("Motors", motor1, ",", motor4)

    # Limit to 20 frames per second.
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()