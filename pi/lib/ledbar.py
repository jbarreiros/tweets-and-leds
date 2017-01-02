"""Control the LEDs"""

import time
import logging
import threading
import RPi.GPIO as GPIO

def set_interval(interval, func, *args):
    """Execute a function every x seconds"""
    stopped = threading.Event()
    def loop():
        while not stopped.wait(interval):
            func(*args)
    threading.Thread(target=loop).start()
    return stopped.set

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

    def start(self, **kwargs):
        pass

    def stop(self):
        pass

    def turn_off_all_leds(self):
        for led in self.series:
            led.off()

class ThresholdLedBar(LedBar):
    def __init__(self, leds):
        super(ThresholdLedBar, self).__init__(leds)
        self.ticks_per_led = 0
        self.ticks = 0
        self.stop_tick_down = lambda: None

    def __del__(self):
        self.stop()

    def start(self, **kwargs):
        threshold = kwargs.get('threshold')

        # clear current ticks and threshold
        self.stop()
        self.ticks = 0

        # start new threshold
        self.ticks_per_led = len(self.series) / float(threshold)
        self.stop_tick_down = set_interval(1, self.tick_down)
        logging.info("New threshold: " + str(threshold) + " (" + str(self.ticks_per_led) + " per LED)")

    def stop(self):
        logging.info("Stopping ThresholdLedBar")
        self.stop_tick_down()
        self.turn_off_all_leds()

    def tick_down(self):
        logging.info("Stepping down from " + str(self.ticks))
        if self.ticks > 0:
            self.ticks -= 1
        self.update_leds()

    def tick(self):
        """Increment tweets counter and adjust LEDs if threshold met"""
        self.ticks += 1
        logging.info("Ticks incremented to " + str(self.ticks))
        self.update_leds()

    def update_leds(self):
        num_leds_on = int(self.ticks * self.ticks_per_led)
        logging.info("Number of LEDs to light is " + str(num_leds_on))
        for idx, led in enumerate(self.series):
            if idx < num_leds_on:
                led.on()
            else:
                led.off()

class SequenceLedBar(LedBar):
    """Blink each LED in succession"""

    def __init__(self, leds):
        super(SequenceLedBar, self).__init__(leds)

    def start(self, **kwargs):
        for led in self.series:
            led.on()
            time.sleep(0.2)
            led.off()

class CylonLedBar(LedBar):
    """Blink each LED from left to right, then right to left"""

    def __init__(self, leds):
        super(CylonLedBar, self).__init__(leds)

    def start(self, **kwargs):
        i = 0
        max_i = (len(self.series) - 1)

        while True:
            self.series[i].on()

            if i == 0:
                self.series[max_i].off()
            elif i > 0:
                self.series[i-1].off()

            time.sleep(0.1)
            i = i + 1

            if i > max_i:
                self.series.reverse()
                i = 0
