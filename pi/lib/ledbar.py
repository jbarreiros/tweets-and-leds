"""Control the LEDs"""

import time
import logging
import RPi.GPIO as GPIO

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

class LedBar(object):
    """Control a series of LEDs"""

    def __init__(self, leds):
        GPIO.setmode(GPIO.BCM)
        self.series = [Led(x) for x in leds]

    def __del__(self):
        logging.info("cleaning up LEDs")
        GPIO.cleanup()

class ThresholdLedBar(LedBar):
    def __init__(self, leds):
        super(ThresholdLedBar, self).__init__(leds)
        self.threshold = 30
        self.ticks = 0

    def start(self, threshold):
        """Resets the LEDs"""
        self.threshold = threshold
        self.ticks = 0
        for led in self.series:
            led.off()

    def tick(self):
        """Increment tweets counter and adjust LEDs if threshold met"""
        self.ticks += 1

class SequenceLedBar(LedBar):
    """Blink each LED in succession"""

    def __init__(self, leds):
        super(SequenceLedBar, self).__init__(leds)

    def start(self):
        for led in self.series:
            led.on()
            time.sleep(0.2)
            led.off()

class CylonLedBar(LedBar):
    """Blink each LED from left to right, then right to left"""

    def __init__(self, leds):
        super(CylonLedBar, self).__init__(leds)

    def on(self, *leds):
        for led in leds:
            led.on()

    def off(self, *leds):
        for led in leds:
            led.off()

    def start(self):
        i = 0
        max_i = (len(self.series) - 1)

        while True:
            self.on(self.series[i])

            if i == 0:
                self.off(self.series[max_i])
            elif i > 0:
                self.off(self.series[i-1])

            time.sleep(0.1)
            i = i + 1

            if i > max_i:
                self.series.reverse()
                i = 0
