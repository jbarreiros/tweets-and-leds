import RPi.GPIO as GPIO

class Led():
    def __init__(self, ledNum):
        self.led = ledNum
        GPIO.setup(self.led, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.led, True)

    def off(self):
        GPIO.output(self.led, False)
