"""Websocket handler"""

import json
import logging
import tornado.websocket
import tweepy

from lib.ledbar import LedBar
from lib.listener import TwitterStreamListener

class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Websocket handler"""

    def initialize(self, config):
        logging.info("initializing websocket")
        # self.led_bar = LedBar(config['led_gpio_pins'])
        self.twitter_stream = self.init_twitter_stream(config['twitter_api'])

    def __del__(self):
        logging.info("Disconnecting twitter stream")
        self.twitter_stream.disconnect()

    def init_twitter_stream(self, api_keys):
        """Initializes twitter Stream object"""
        auth = tweepy.OAuthHandler(api_keys['ckey'], api_keys['csecret'])
        auth.set_access_token(api_keys['atoken'], api_keys['asecret'])

        listener = TwitterStreamListener(api=None, on_status_callback=self.on_tweet)
        return tweepy.Stream(auth, listener)

    def on_tweet(self, tweet):
        """TwitterStreamListener callback"""
        self.write_message(json.dumps(tweet._json))
        # self.led_bar.tick()

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("Websocket opened")

    def on_message(self, message):
        logging.info("Received websocket message: " + message)
        data = json.loads(message)
        self.twitter_stream.disconnect()
        self.twitter_stream.filter(track=[data['keyword']], async=True)
        self.write_message(json.dumps({"success": True}))

    def on_close(self):
        logging.info("Websocket closed")
        self.twitter_stream.disconnect()
