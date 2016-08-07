#https://pinout.xyz/

import json
import RPi.GPIO as GPIO
import tweepy
from Led import Led
from Listener import Listener

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

GPIO.setmode(GPIO.BCM)
leds = [Led(17), Led(27), Led(22)]

auth = tweepy.OAuthHandler(config['twitterApi']['ckey'], config['twitterApi']['csecret'])
auth.set_access_token(config['twitterApi']['atoken'], config['twitterApi']['asecret'])

listener = Listener(leds)

twitterStream = tweepy.Stream(auth, listener)
twitterStream.filter(track=['javascript'])
