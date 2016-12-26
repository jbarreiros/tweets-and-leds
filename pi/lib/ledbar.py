"""Control the LEDs"""

import time
import RPi.GPIO as GPIO

class LedBar(object):
    """Control a series of LEDs"""

    def __init__(self, *leds):
        GPIO.setmode(GPIO.BCM)
        self.series = [Led(x) for x in leds]

    def __del__(self):
        print 'cleaning up LEDs'
        GPIO.cleanup()

    def sequence_blink(self):
        """Blink each LED in succession"""

        for led in self.series:
            led.on()
            time.sleep(0.2)
            led.off()

    def parallel_blink(self):
        """Blink all LEDs at the same time"""

        for led in self.series:
            led.on()
        time.sleep(0.2)
        for led in self.series:
            led.off()

class Led(object):
    """Control a single LED"""

    def __init__(self, ledNum):
        self.led = ledNum
        GPIO.setup(self.led, GPIO.OUT)
        self.off()

    def on(self):
        """Switch LED on"""
        GPIO.output(self.led, True)

    def off(self):
        """ Switch LED off"""
        GPIO.output(self.led, False)
