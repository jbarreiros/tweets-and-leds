"""Twitter stream listener"""

import json
from tweepy.streaming import StreamListener

class Listener(StreamListener):
    """Twitter stream listener"""

    def __init__(self, leds):
        print "listening for tweets"
        self.leds = leds

    def on_data(self, data):
        """Callback for when a tweet is received"""
        all_data = json.loads(data)
        tweet = all_data['text']
        print tweet
        #self.leds.parallel_blink()
        self.leds.sequence_blink()
        return True

    @classmethod
    def on_error(cls, status):
        """Error handler"""
        print status
        return False
