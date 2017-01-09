"""
Tweets and LEDs
A silly little application to blink leds based on tweets.
"""

import os
import sys
import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tweepy

from lib.websocket import WebsocketHandler
from lib.ledbar import ThresholdLedBar
from lib.listener import TwitterStreamListener

logging.basicConfig(level=logging.DEBUG)

class IndexHandler(tornado.web.RequestHandler):
    """Serves the index page"""
    @tornado.web.asynchronous
    def get(self):
        self.render('../www/build/index.html')

def main():
    """Main"""
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    parent_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
    root_dir = os.path.join(parent_dir, 'www/build')
    static_dir = os.path.join(parent_dir, 'www/build/static')

    # websocket clients
    clients = set()

    # led bar controller
    led_bar = ThresholdLedBar(config['led_gpio_pins'])

    # twitter stream
    twitter_auth = tweepy.OAuthHandler(config['twitter_api']['ckey'], config['twitter_api']['csecret'])
    twitter_auth.set_access_token(config['twitter_api']['atoken'], config['twitter_api']['asecret'])
    twitter_stream_listener = TwitterStreamListener(clients=clients, led_bar=led_bar)
    twitter_stream = tweepy.Stream(twitter_auth, twitter_stream_listener)

    # tornado settings
    settings = {
        "debug": config['debug'],
    }

    # tornado routes
    urls = [
        (r'/', IndexHandler),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, dict(path=root_dir)),
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=static_dir)),
        (r'/ws', WebsocketHandler, dict(clients=clients, led_bar=led_bar, stream=twitter_stream)),
    ]

    application = tornado.web.Application(urls, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(config['websocket']['port'])

    logging.info('Starting Tornado!')

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logging.info("Closing app...")
        twitter_stream.disconnect()
        logging.info("Stream disconnected!")
        led_bar.stop()
        logging.info("LED bar reset")
        sys.exit(0)

if __name__ == '__main__':
    main()
