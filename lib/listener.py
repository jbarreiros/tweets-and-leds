import json
from tweepy.streaming import StreamListener

class Listener(StreamListener):
    def __init__(self, leds):
        print "listening for tweets"
        self.leds = leds

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data['text']
        print(tweet)
        #self.leds.parallel_blink()
        self.leds.sequence_blink()
        return(True)

    def on_error(self, status):
        print (status)
        return false
