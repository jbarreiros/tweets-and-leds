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

from lib.websocket import WebsocketHandler

logging.basicConfig(level=logging.DEBUG)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('../www/build/index.html')

def main():
    """Main"""
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    parentDir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
    rootDir = os.path.join(parentDir, 'www/build')
    staticDir = os.path.join(parentDir, 'www/build/static')

    settings = {
        "debug": config['debug'],
    }

    urls = [
        (r'/', IndexHandler),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, dict(path=rootDir)),
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=staticDir)),
        (r'/ws', WebsocketHandler, dict(config=config)),
    ]

    application = tornado.web.Application(urls, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(config['websocket']['port'])

    logging.info('Starting Tornado!')

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
