"""Twitter stream listener"""

import json
import logging
import tweepy.streaming

class TwitterStreamListener(tweepy.streaming.StreamListener):
    """Twitter stream listener"""

    def __init__(self, api=None, **kwargs):
        logging.info("Instantiating twitter stream listener")
        super(TwitterStreamListener, self).__init__(api)
        self.clients = kwargs.get('clients')
        self.led_bar = kwargs.get('led_bar')

    def on_status(self, status):
        """Callback for when a tweet is received"""
        logging.info("Received tweet: " + status.text)

        for client in self.clients:
            client.write_message(json.dumps({
                'event': 'new_tweet',
                'id': status.id,
                'text': status.text,
            }))

        self.led_bar.tick()

    def on_error(self, status_code):
        """Error handler"""
        logging.error("Twitter stream listener error: " + status_code)
        if status_code == 420:
            return False
