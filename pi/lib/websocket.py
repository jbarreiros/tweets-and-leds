"""Websocket handler"""

import tornado.websocket

class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Websocket handler"""

    def check_origin(self, origin):
        return True

    def open(self):
        print("Websocket opened.")

    def on_message(self, message):
        self.write_message("You said: " + message)

    def on_close(self):
        print("Websocket closed.")
