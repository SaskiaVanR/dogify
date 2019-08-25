#!/usr/bin/env python3

import tweepy
import urllib.request
import sys
import platform
import os

# DO NOT COMMIT API KEYS TO GITHUB YOU IDIOT
secretfile = open("secrets.txt", "r")
secrets = secretfile.read().splitlines()
consumer_key = secrets[0]
consumer_secret = secrets[1]
access_token = secrets[2]
access_token_secret = secrets[3]

# Set up tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#api.update_status("Hello dog!")

# Get last replied to tweet from file
try:
    file_since = open("twitter_since_id.txt", "r")
    since_id = int(file_since.read())
    file_since.close()
except:
    print("Warning: couldn't read twitter_since_id.txt")
    since_id = 1

# Check mentions
for tweet in tweepy.Cursor(api.mentions_timeline,since_id).items():
    # Check if tweet has an image attached
    if 'media' in tweet.entities:
        print(tweet.text)
        url = tweet.entities.get('media', [])[0]['media_url']
        media = urllib.request.urlopen(url).read()
        media_filename = "current_tweet." + url.split('.')[-1]
        media_file = open(media_filename, "wb")
        media_file.write(media)
        media_file.close()
        if platform.system() == "Windows":
            os.system("\Python37\python.exe evolvedog.py " + media_filename)
        else:
            os.system("./evolvedog.py " + media_filename)
        statsfile = open("stats_" + media_filename + ".txt", "r")
        api.update_with_media("dogified_" + media_filename, "Here is your dog! " + statsfile.read(), in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        statsfile.close()
        print("Tweet sent!")
        os.remove(media_filename)
        os.remove("dogified_" + media_filename)
        os.remove("stats_" + media_filename + ".txt")
    # Check if tweet is in reply to another tweet (that may have an image)
    #TODO
    # Update most recently processed image
    since_id = max(tweet.id, since_id)





# Write last replied to tweet to text file
try:
    file_since = open("twitter_since_id.txt", "w")
    file_since.write(str(since_id))
    file_since.close()
except:
    print("Warning: couldn't write twitter_since_id.txt")
