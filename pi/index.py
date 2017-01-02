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

    settings = {
        "debug": config['debug'],
    }

    urls = [
        (r'/', IndexHandler),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, dict(path=root_dir)),
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=static_dir)),
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
