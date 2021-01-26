import math
from gusbots import speedEstimator
from gusbots.controller import GoToGoal

class Inputs():
    ''' State machine inputs '''

    autonomous = 0     # change state to autonomous mode (GoToGoal behavior)
    joy_left = 0       # value of the left joystick
    joy_right = 0      # value of the right joystick
    x = 0              # x-position of the robot
    y = 0              # y-position of the robot
    theta = 0          # robot orientation
    dt = 0             # time delta between the last execution (used by the PID)
    el = 0             # left encoder instance
    er = 0             # right endoer instance
    L = 0              # distance between the wheels

class Outputs():
    ''' State machine outputs '''

    left_motor = 0     # left motor output (0..1)
    right_motor = 0    # right motor ouput (0..1)

class State():
    ''' When creating a new state, extend this class '''

    def run(self, input, output):
        pass
    
    def entry(self, input, output):
        pass
    
    def exit(self, input, output):
        pass

######################################
# States
######################################

class InitSt(State):
    name = "Init"

    def __init__(self):
        pass
        
    def run(self, input, output):
        return ManualSt.name

class ManualSt(State):
    '''
        Manual state - allow the robot to be controller by the joystick.
    '''
    name = "Manual"
    
    def entry(self, input, output):
        print("Manual mode state")

    def run(self, input, output):
        next_state = ManualSt.name
        
        output.left_motor = input.joy_left
        output.right_motor = input.joy_right

        if (input.autonomous == 1):
            next_state = GoToGoalSt.name
        
        return next_state

class GoToGoalSt(State):
    '''
        Go to Goal State - Robot go to a specific goal autonomously. The goal change
        every state entry.
    '''
    name = "GoToGoal"
    next_goal = 0
    array_of_goals = [[1,0]]
    
    def entry(self, input, output):
        # Set goal and next goal (in the next entry)
        self.goal = GoToGoalSt.array_of_goals[GoToGoalSt.next_goal]
        GoToGoalSt.next_goal =(GoToGoalSt.next_goal+1)%len(GoToGoalSt.array_of_goals)
        print("GoToGoal state", self.goal, GoToGoalSt.next_goal)

        # Initiate rate limit variable (assume that the robot is always stopped when
        # entering autonomous mode)
        self.leftPrevCmd = 0
        self.rightPrevCmd = 0

        # Create an instance of the PID controller
        self.controller = GoToGoal.GoToGoal()

    def limit(self, value, downLimit, upLimit):
        return upLimit if value >= upLimit else downLimit if value <= downLimit else value

    def rateLimit(self, value, ctrlVar, upLimit, downLimit):
        ctrlVar = self.limit(value, (downLimit + ctrlVar),(upLimit + ctrlVar))
        return ctrlVar

    def run(self, input, output):
        next_state = GoToGoalSt.name
        
        # Run controller
        w = self.controller.step(self.goal[0], self.goal[1], input.x, input.y, input.theta, input.dt)
        
        # Estimate the motor outpus with fixed speed of 0.05
        left, right = speedEstimator.uni_to_diff(0.03, w, input.el,input.er,input.L)
        
        # Apply rate limits to the speed and make sure it is between 0 and 1
        print('Motor commands from PID: left, right', left, right)

        if left > right:
            left2 = left/left
            right2 = right/left
        else:
            left2 = left/right
            right2 = right/right
        
        print('left 2, right 2', left2, right2)

        left3 = self.rateLimit(left2, self.leftPrevCmd, 0.1, -0.1)
        right3 = self.rateLimit(right2, self.rightPrevCmd, 0.1, -0.1)
        left3 = left3 if left3 >=0.5 else 0.5
        right3 = right3 if right3 >= 0.5 else 0.5
        
        self.leftPrevCmd = left3
        self.rightPrevCmd = right3
        print("left3, right 3", left3, right3)
        
        # Make sure ouputs are not negative (robot can not reverse yet)
        left2 = left2 if left2 >= 0 else 0
        right2 = right2 if right2 >=0 else 0
        output.left_motor = left3
        output.right_motor = right3
        print('GoToGoal outputs:', output.left_motor, output.right_motor)
        
        # Check if it is in the goal. If yes, change state
        if (abs(input.x - self.goal[0]) < 0.08 and
            abs(input.y - self.goal[1]) < 0.08):
            next_state = AtTheGoalSt.name

        # Go back to manual mode if autonomous is off
        if (input.autonomous == 0):
            next_state = ManualSt.name
        
        return next_state

class AtTheGoalSt(State):
    '''
        At the Goal state
    '''
    name = "AtTheGoal"
    
    def entry(self, input, output):
        print("AtTheGoal state")
        output.left_motor = 0
        output.right_motor = 0
    
    def run(self, input, output):
        next_state = AtTheGoalSt.name
        
        output.left_motor = 0
        output.right_motor = 0
        #print('at the goal')
        
        if (input.autonomous == 0):
            next_state = ManualSt.name
        
        return  next_state

######################################
# Main control
######################################

class stateControl():
    '''
        Main class to constrol the state
    '''
    def __init__(self):
        self.states = {
        InitSt.name: InitSt(), 
        ManualSt.name:ManualSt(),
        GoToGoalSt.name: GoToGoalSt(),
        AtTheGoalSt.name: AtTheGoalSt()}
        
        self.input = Inputs()
        self.output = Outputs()
        self.currentState = InitSt.name
        self.states[self.currentState].entry(self.input, self.output)

    def step(self):
        next_state = self.states[self.currentState].run(self.input, self.output)
        
        if (next_state != self.currentState):
            self.states[self.currentState].exit(self.input, self.output)
            self.currentState = next_state
            self.states[self.currentState].entry(self.input, self.output)
