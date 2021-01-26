from gusbots.sensorInterruption import SensorInterruption

class encoder():
    def __init__(self, pin, ticks_p_revol, radius):
        self.counter = 0
        self.ticks_p_revol = ticks_p_revol
        self.radius = radius
        
        self.int = SensorInterruption(pin, self.count)

    def count(self, value):
        '''
            Callback function for GPIO interruption
        '''
        self.counter += 1
    
    def reset(self):
        self.counter = 0
