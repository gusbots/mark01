import math

class speedEstimator():

    def __init__(self, el, er, R, L):
        '''
            Initialize speed estimator
            
            el - left wheel encoder
            er - right wheel encoder
            R - radious of the wheels in meters
            L - distance  between the wheels in meters
        '''
        self.el = el
        self.er = er
        self.R = R
        self.L = L
        self.wl_last_counter = 0
        self.wr_last_counter = 0
        
        # Speed converter for rpm
        self.wl_speed_rpm = (60/self.el.ticks_p_resol) * 10**9
        self.wr_speed_rpm = (60/self.er.ticks_p_resol) * 10**9

    def wheelSpeed(self, dt, left_direction=1, right_direction=1):
        '''
            Calculate wheel speeds. Call this function between 50ms to 200ms.
            
            dt - time delta since last read (in ns)
            left_direction - the direction the left motor is spinning
            right_direction = the direction the right motor is spinning
        '''
        wl_delta_ticks = self.el.counter - self.wl_last_counter
        wr_delta_ticks = self.er.counter - self.wr_last_counter

        self.wl_last_counter = self.el.counter
        self.wr_last_counter = self.er.counter

        left_wheel_speed = left_direction * wl_delta_ticks/dt * self.wl_speed_rpm
        right_wheel_speed = right_direction * wr_delta_ticks/dt * self.wr_speed_rpm

        return (left_wheel_speed, right_wheel_speed)

    def robotSpeed(self, left_rpm, right_rpm):
        left_rad_s = math.pi/30 * left_rpm
        right_rad_s = math.pi/30 * right_rpm

        v = self.R/2 * (right_rad_s + left_rad_s)
        w = self.R/self.L * (right_rad_s - left_rad_s)

        return v, w

def uni_to_diff(v,w, el, er, L):

    vel_r = (2 * v + w * L)/(2 * er.radius);
    vel_l = (2 * v - w * L)/(2 * el.radius);
    
    return vel_l, vel_r