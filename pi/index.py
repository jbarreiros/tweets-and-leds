"""
Tweets and LEDs
A silly little application to blink leds based on tweets.
"""

import json
import tweepy
from lib.ledbar import LedBar
from lib.listener import Listener

def main():
    """Initializes LEDs and kicks off twitter Stream"""

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    api_keys = config['twitterApi']
    leds = LedBar(14, 15, 18, 23, 24, 25, 8, 7)

    auth = tweepy.OAuthHandler(api_keys['ckey'], api_keys['csecret'])
    auth.set_access_token(api_keys['atoken'], api_keys['asecret'])

    listener = Listener(leds)

    twitter_stream = tweepy.Stream(auth, listener)
    twitter_stream.filter(track=['javascript'])

if __name__ == '__main__':
    main()
