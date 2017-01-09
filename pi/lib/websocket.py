"""Websocket handler"""

import json
import logging
import tornado.websocket

class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Websocket handler"""

    active_client = None
    """The client that set the current keyword and threshold"""

    keyword = None
    """The keyword currently being used to filter the stream"""

    threshold = None
    """The threshold currently being used to on the ledbar"""

    def initialize(self, clients, led_bar, stream):
        logging.info("initializing websocket")
        self.clients = clients
        self.led_bar = led_bar
        self.twitter_stream = stream

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("Websocket opened")

        self.clients.add(self)

        if WebsocketHandler.keyword != None:
            self.notify(self.get_current_config_message())

    def on_close(self):
        logging.info("Websocket closed")
        self.clients.remove(self)

    def on_message(self, message):
        logging.info("Received websocket message: " + message)
        data = json.loads(message)

        if data['event'] == 'stop':
            WebsocketHandler.keyword = None
            WebsocketHandler.threshold = None
            self.twitter_stream.disconnect()
            self.led_bar.stop()
            self.notify({'event': 'stop', 'success': True})

        elif data['event'] == 'set_keyword':
            self.twitter_stream.disconnect()
            self.led_bar.start(threshold=data['threshold'])
            self.twitter_stream.filter(track=[data['keyword']], async=True)
            WebsocketHandler.keyword = data['keyword']
            WebsocketHandler.threshold = data['threshold']
            self.notify({'event': 'set_keyword', 'success': True})

        self.broadcast(self.get_current_config_message())

    def get_current_config_message(self):
        return {
            'event': 'current_config',
            'keyword': WebsocketHandler.keyword,
            'threshold': WebsocketHandler.threshold
        }

    def notify(self, data):
        payload = json.dumps(data)
        self.write_message(payload)

    def broadcast(self, data):
        """Sends message to every connected client"""
        payload = json.dumps(data)
        for client in self.clients:
            try:
                client.write_message(payload)
            except tornado.websocket.WebSocketClosedError:
                logging.error("Error sending websocket message", exc_info=True)
