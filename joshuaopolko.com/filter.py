#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymysql
import json
import time
import datetime

# Create a connection object
dbServerName    = "127.0.0.1"
dbUser          = ""
dbPassword      = ""
dbName          = "twitter"
charSet         = "utf8mb4"

#conn   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet)

conn   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet)

c = conn.cursor()

# Auth
consumer_key = ''
consumer_secret         = ''
access_token            = ''
access_token_secret     = ''

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            tweet_id = json.loads(data)['id']
        except:
            tweet_id = 'NULL'
        screen_name = json.loads(data)['user']['screen_name']
        screen_name = (screen_name)
        born = json.loads(data)['user']['created_at']
        tweet_date = json.loads(data)['created_at']
        tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y'))
        description = (json.loads(data)['user']['description'])
        username = json.loads(data)['user']['name']
        username = username
        text = json.loads(data)['text']
        text = text.lower()
        try:
            source = json.loads(data)['source'].split(">")[-2].replace("</a", "")
        except:
            source = 'NULL'

        location = json.loads(data)['user']['location']
        time_zone = json.loads(data)['user']['time_zone']
        utc_offset = json.loads(data)['user']['utc_offset']
        user_id = json.loads(data)['user']['id']
        profurl = ("https://twitter.com/%s" % username)
        profile_img = json.loads(data)['user']['profile_image_url'].replace("_normal.",".")
        link_color = json.loads(data)['user']['profile_link_color']
        in_reply_to_screen_name = json.loads(data)['in_reply_to_screen_name']
        if 'profile_banner_url' in json.loads(data)['user']:
            banner_url = json.loads(data)['user']['profile_banner_url']
        else:
            banner_url = 'na'
        print(screen_name,text)
        c.execute("replace INTO twitter.overnight (tweet_id, screen_name, tweet_at, description, username, text, source, location, time_zone, utc_offset, user_id, profurl, profile_img, link_color, banner_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (tweet_id, screen_name, tweet_at, description, username, text, source, location, time_zone, utc_offset, user_id, profurl, profile_img, link_color, banner_url))
        #print(screen_name, json.loads(data)['user']['url'])
        conn.commit()
    def on_error(self, status):
        print(statuss)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    #stream.filter(follow=[''], track=[''], async=True)
    #stream.filter(track=['#covidiot','#whitegenocide','#BLM','#blacklivesmatter','#islamophobia'], is_async=True)
    stream.filter(track=['#bluelivesmatter','#covid19','#cryptocurrency','#covidiot', '#whitegenocide', '#BLM', '#blacklivesmatter', '#islamophobia', '#protestlockdown'], async=True)
