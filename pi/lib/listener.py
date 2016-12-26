"""Twitter stream listener"""

import logging
import tweepy.streaming

class TwitterStreamListener(tweepy.streaming.StreamListener):
    """Twitter stream listener"""

    def __init__(self, api=None, **kwargs):
        logging.info("Instantiating twitter stream listener")
        super(TwitterStreamListener, self).__init__(api)
        self.on_status_callback = kwargs.get('on_status_callback')

    def on_status(self, status):
        """Callback for when a tweet is received"""
        logging.info("Received tweet: " + status.text)
        self.on_status_callback(status.text)

    def on_error(self, status_code):
        """Error handler"""
        logging.error("Twitter stream listener error: " + status_code)
        if status_code == 420:
            return False
