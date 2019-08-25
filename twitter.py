#!/usr/bin/env python3

import tweepy

# DO NOT COMMIT API KEYS TO GITHUB YOU IDIOT
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Set up tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status("Hello dog!")
