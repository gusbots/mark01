import pygame

'''
PS4 Controller MAP

Buttons:
    0 - Square
    1 - X
    2 - Circle
    3 - Triangle
    4 - L1
'''
# Initialize pygame (used to read the joystick)
pygame.init()

# Initialize the joysticks.
pygame.joystick.init()

# Joystick modes
TANK_MODE = 0
ARCADE_MODE = 1

class create:

    def __init__(self, joystickIndex=0, mode=ARCADE_MODE):
        '''
        joystickIndex: Use the showAvailable function to verify all the index of all the
                       joysticks connected to the system and pass the index here to use it.
        mode:          select TANK_MODE or ARCADE_MODE
        '''
        self.joy = pygame.joystick.Joystick(joystickIndex)
        self.joy.init()
        self.axes = self.joy.get_numaxes()
        self.buttons = self.joy.get_numbuttons()
        self.mode = mode
        self.R2NeverPressed = True
        self.L2NeverPressed = True
        self.switchModePressed = False
        self.autonomousModePressed = False
        
        self.autonomous = 0
        self.resetPose = False


    def tankMode(self):
        for i in range(self.axes):
            axis = self.joy.get_axis(i)
            # Left stick up/down (right wheel)
            if i == 1:
                if axis < 0.3 and axis > -0.3:
                    axis = 0
                leftMotor = axis

            # Right stick up/down (left wheel)
            if i == 5:
                if axis < 0.3 and axis > -0.3:
                    axis = 0
                rightMotor = axis
                
            if i == 3:
                if axis != 0:
                    self.R2NeverPressed = False
            if i == 4:
                if axis != 0:
                    self.L2NeverPressed = False
                
        return leftMotor, rightMotor


    def arcadeMode(self):
        # Reset motor commands before reading new joystick inputs
        leftMotor = 0
        rightMotor = 0
    
        for i in range(self.axes):
            axis = self.joy.get_axis(i)
            
            # R2
            # When never pressed R2 has a value of 0. After the first use, when released,
            # R2 has a value of -1. When full pressed it has a value of 1.
            if i == 3:
                # Check if pressed for the first time
                if self.R2NeverPressed == True and axis != 0:
                    self.R2NeverPressed = False
                
                if self.R2NeverPressed == False:
                    if axis < 0.3 and axis > -0.3:
                        axis = 0

                    leftMotor = leftMotor + (axis + 1)/2
                    rightMotor = rightMotor + (axis + 1)/2

            # L2
            # When never pressed L2 has a value of 0. After the first use, when released,
            # L2 has a value of -1. When full pressed it has a value of 1.
            if i == 4:
                # Check if pressed for the first time
                if self.L2NeverPressed == True and axis != 0:
                    self.L2NeverPressed = False
                
                if self.L2NeverPressed == False:
                    if axis < 0.3 and axis > -0.3:
                        axis = 0

                    leftMotor = leftMotor - (axis + 1)/2
                    rightMotor = rightMotor - (axis + 1)/2

            # Left stick left/right
            if i == 0:
                if axis < 0.3 and axis > -0.3:
                    axis = 0
            
                if leftMotor >= 0:
                    leftMotor = leftMotor - axis
                else:
                    leftMotor = leftMotor + axis
                    
                if rightMotor >=0:
                    rightMotor = rightMotor + axis
                else:
                    rightMotor = rightMotor - axis   

            # Limit the output between -1 and 1
            if leftMotor > 1:
                leftMotor = 1
            
            if rightMotor > 1:
                rightMotor = 1
                
            if leftMotor < -1:
                leftMotor = -1
            
            if rightMotor < -1:
                rightMotor = -1
        
        return leftMotor, rightMotor


    def readButtons(self):
        for i in range(self.buttons):
            button = self.joy.get_button(i)
            # Button 13 is the big black button in the middle of the joystick (usually used for maps)
            # The switchModePressed variable is used to detect the transition from not pressed to pressed
            if i == 13 and button == 1 and self.switchModePressed == False:
                self.switchMode()
                self.switchModePressed = True
            if i == 13 and button == 0 and self.switchModePressed == True:
                self.switchModePressed = False
            
            # Button 0 (square) is to reset the pose of the robot (x, y, theta) values
            if i == 0:
                self.resetPose = button
            
            # Button 1 (x) is to go on/off from autonomous mode
            if i == 1 and button == 1 and self.autonomousModePressed == False:
                self.autonomous = 1 - self.autonomous
                self.autonomousModePressed = True
            if i == 1 and button == 0 and self.autonomousModePressed == True:
                self.autonomousModePressed = False
                


    def tick(self):
        for event in pygame.event.get(): # User did something.
            pass

        self.readButtons()
        
        if self.mode == TANK_MODE:
            return self.tankMode()
        else:
            return self.arcadeMode()


    def switchMode(self):
        self.mode += 1
        self.mode = self.mode % 2 # Limit the mode between 0 and 1


def showAvailable():
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
