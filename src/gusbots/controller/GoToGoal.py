import math

class GoToGoal:

    def __init__(self):
        self.E_d = 0
        self.E_i = 0

        # PID gains
        self.Kp = 1.5
        self.Ki = 0.01
        self.Kd = 0.5
    
    def step(self, x_g, y_g, x, y, theta, dt):

        dt = dt/1000000000
        
        # Distance between goal and robot in x direction
        u_x = x_g - x
        
        # Distance between goal and robot in y direction
        u_y = y_g - y
        
        if (abs(u_x) < 0.05 and abs(u_y < 0.05)):
            print("GOoooOOOOOlLLL", x, y)
            return 0
        
        # Angle from robot to goal
        theta_g = math.atan2(u_y, u_x)
        
        # Error between the goal angle and robot's angle
        e_k = theta_g - theta
        e_k = math.atan2(math.sin(e_k), math.cos(e_k))
        
        # Error for the proportional term
        e_P = e_k
        
        # Error for the integral term.
        e_I = self.E_i + e_k * dt
                 
        # Error for the derivative term.
        e_D = (e_k - self.E_d)/dt

        w = self.Kp * e_P + self.Ki * e_I + self.Kd * e_D
        print("Distance from goal", '{:02.3f}'.format(u_x), '{:02.3f}'.format(u_y),
        '{:02.3f}'.format(theta_g), '{:02.3f}'.format(e_k),
        '{:02.3f}'.format(e_P), '{:02.3f}'.format(e_I),
        '{:02.3f}'.format(e_D), '{:02.3f}'.format(w), '{:02.3f}'.format(dt))

        # Save errors for next time step
        self.E_i = e_I
        self.E_d = e_k

        return w