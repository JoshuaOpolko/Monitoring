#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import MySQLdb
import json
import time
import datetime
from keys import keys


conn = MySQLdb.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
c = conn.cursor()

# Auth
consumer_key = keys['consumer_key']
consumer_secret         = keys['consumer_secret']
access_token            = keys['access_token']
access_token_secret     = keys['access_token_secret']

class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet_id = json.loads(data)['id']
        screen_name = json.loads(data)['user']['screen_name']
        screen_name = (screen_name)
        born = json.loads(data)['user']['created_at']
        tweet_date = json.loads(data)['created_at']
        tweet_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet_date,'%a %b %d %H:%M:%S +0000 %Y'))
        description = (json.loads(data)['user']['description'])
        username     = json.loads(data)['user']['name']
        username = str(username)
        text     = json.loads(data)['text']
        text = text.lower()
        source = json.loads(data)['source'].split(">")[-2].replace("</a","")
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
        #print(screen_name, json.loads(data)['user'])
        c.execute("replace INTO twitter.overnight (screen_name, username, in_reply_to_screen_name, tweet_at, description,text,source,location,time_zone, utc_offset, user_id, tweet_id, logged, profile_img, banner_url, link_color, url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (str(screen_name).encode("utf8","ignore"), str(username).encode("utf8","ignore"), in_reply_to_screen_name, tweet_at, str(description).encode("utf8","ignore"),text.encode("utf-8"), source,location, time_zone, utc_offset, user_id, tweet_id, datetime.datetime.now(), profile_img, banner_url, link_color, json.loads(data)['user']['url']))
        print(screen_name, json.loads(data)['user']['url'])
        conn.commit()        
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    #stream.filter(follow=[''], track=[''], async=True)
    stream.filter(track=['Klaudusz','Briere'], async=True)
