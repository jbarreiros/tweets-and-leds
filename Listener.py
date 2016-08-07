import RPi.GPIO as GPIO
import time
import json
from tweepy.streaming import StreamListener

class Listener(StreamListener):
    def __init__(self, leds):
        self.leds = leds

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data['text']
        print(tweet)
        #self.parallel_blink()
        self.sequence_blink()
        return(True)

    def on_error(self, status):
        print (status)
        if status == 420:
            GPIO.cleanup()
        return false

    def sequence_blink(self):
        for led in self.leds:
            led.on()
            time.sleep(0.2)
            led.off()

    def parallel_blink(self):
        map(lambda x:x.on(), self.leds)
        time.sleep(0.2)
        map(lambda x:x.off(), self.leds)
