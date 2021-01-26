import math

class odometry():

    def __init__(self, el, er, L):
        '''
            Initialize odometry
            
            el - left wheel encoder
            er - right wheel encoder
            L - distance  between the wheels in meters
        '''
        self.el = el
        self.er = er
        self.L = L
        self.wl_last_counter = 0
        self.wr_last_counter = 0
        
        self.x = 0
        self.y = 0
        self.theta = 0
        
        # Calculate meters per tick
        self.meters_per_tick_left = (2 * math.pi * self.el.radius) / (el.ticks_p_revol)
        self.meters_per_tick_right = (2 * math.pi * self.er.radius) / (er.ticks_p_revol)

    def step(self, left_direction=1, right_direction=1):
        '''
            Call this function periodically to update robot pose estimiation.
        '''
        # Calculate the delta for ticks since last read
        delta_ticks_left = (self.el.counter - self.wl_last_counter) * left_direction
        delta_ticks_right = (self.er.counter - self.wr_last_counter) * right_direction
        
        # Update counters to next read
        self.wl_last_counter = self.el.counter
        self.wr_last_counter = self.er.counter
        
        # Calculate new pose
        Dl = self.meters_per_tick_left * delta_ticks_left
        Dr = self.meters_per_tick_right * delta_ticks_right
        Dc = (Dr + Dl) / 2
        
        x_dt = Dc * math.cos(self.theta)
        y_dt = Dc * math.sin(self.theta)
        theta_dt = (Dr - Dl) / self.L

        self.x = self.x + x_dt
        self.y = self.y + y_dt
        self.theta = self.theta + theta_dt
        
        return self.x, self.y, self.theta
        
    def resetPose(self):
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def getPose(self):
        return self.x, self.y, self.theta