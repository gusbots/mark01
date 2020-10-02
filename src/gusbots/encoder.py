import RPi.GPIO as GPIO

class encoder():
    def __init__(self, pin, ticks_p_resol):
        self.counter = 0
        self.ticks_p_resol = ticks_p_resol

        # Setup GPIO for both edge detections
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.count)

    def count(self, pin):
        '''
            Callback function for GPIO interruption
        '''
        self.counter += 1
