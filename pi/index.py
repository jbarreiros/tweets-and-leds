"""
Tweets and LEDs
A silly little application to blink leds based on tweets.
"""

import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web

from lib.websocket import WebsocketHandler

logging.basicConfig(level=logging.DEBUG)

def main():
    """Main"""
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    application = tornado.web.Application([
        (r"/", WebsocketHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(config['websocket']['port'])
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
