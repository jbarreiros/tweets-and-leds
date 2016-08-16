import RPi.GPIO as GPIO
import time

class LedBar():
    def __init__(self, *leds):
        GPIO.setmode(GPIO.BCM)
        self.series = list(map(lambda x: Led(x), leds))

    def __del__(self):
        print 'cleaning up LEDs'
        GPIO.cleanup()

    def sequence_blink(self):
        for led in self.series:
            led.on()
            time.sleep(0.2)
            led.off()

    def parallel_blink(self):
        map(lambda x: x.on(), self.series)
        time.sleep(0.2)
        map(lambda x: x.off(), self.series)

class Led():
    def __init__(self, ledNum):
        self.led = ledNum
        GPIO.setup(self.led, GPIO.OUT)
        self.off()

    def on(self):
        GPIO.output(self.led, True)

    def off(self):
        GPIO.output(self.led, False)
