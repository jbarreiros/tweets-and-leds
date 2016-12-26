"""
Tweets and LEDs
A silly little application to blink leds based on tweets.
"""

import json
import tweepy
import tornado.httpserver
import tornado.ioloop
import tornado.web

from lib.ledbar import LedBar
from lib.listener import TwitterStreamListener
from lib.websocket import WebsocketHandler

def init_twitter_listener():
    """Initializes LEDs and kicks off twitter Stream"""

    with open('../config.json') as json_data_file:
        config = json.load(json_data_file)

    api_keys = config['twitterApi']
    leds = LedBar(14, 15, 18, 23, 24, 25, 8, 7)

    auth = tweepy.OAuthHandler(api_keys['ckey'], api_keys['csecret'])
    auth.set_access_token(api_keys['atoken'], api_keys['asecret'])

    listener = TwitterStreamListener(leds)

    twitter_stream = tweepy.Stream(auth, listener)
    twitter_stream.filter(track=['javascript'])

def init_websocket():
    """Initialize websocket"""
    application = tornado.web.Application([
        (r"/", WebsocketHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9000)
    tornado.ioloop.IOLoop.instance().start()

def main():
    """Main"""
    init_twitter_listener()
    init_websocket()

if __name__ == '__main__':
    main()
