#!/usr/bin/python3
import tweepy 
import sqlite3
import matplotlib.pyplot as plt
from collections import Counter
from keys import keys
import time

conn = sqlite3.connect(':memory:')

SCREEN_NAME = keys['screen_name']
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,parser=tweepy.parsers.JSONParser())

top_list = ['CristianMtz_G']
top_n = 5

# Create table
c = conn.cursor()
c.execute('''CREATE TABLE tweets (screen_name text, username text, in_reply_to_screen_name text, text text, location text, time_zone text, description text, profile_img text, bg_color text, banner_url text, link_color text, source, followers real, friends real, url text, tweet_at datetime, born datetime, tweet_id real)''')
conn.commit()

for screen_name in top_list:
    screen_name = str(screen_name).replace("@","")
    c = conn.cursor()
    tweets = api.user_timeline(screen_name = screen_name,count=200)
    if (len(tweets)) < 1:
        print("0 Tweets: ", screen_name)
    for tweet in tweets:
        try:
            if 'url' in str(tweet['user']['entities']):
                url = str(tweet['user']['entities']['url']['urls'][0]['expanded_url'])
            else:
                url = 'na'
        except:
            url = 'no_url_found'
        try:
            banner_url = tweet['user']['profile_banner_url']
        except:
            banner_url = 'na'
        if not tweet['user']['location']:
            location = 'na'
        else:
            location = tweet['user']['location']
        c.execute("INSERT INTO tweets (screen_name, username, in_reply_to_screen_name, text, location, time_zone, description, profile_img, bg_color, banner_url, link_color, source, followers, friends, url, tweet_at, born, tweet_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (tweet['user']['screen_name'],tweet['user']['name'],tweet['in_reply_to_screen_name'], tweet['text'], tweet['user']['location'], tweet['user']['time_zone'],tweet['user']['description'],tweet['user']['profile_image_url'],tweet['user']['profile_background_color'], banner_url, tweet['user']['profile_link_color'], tweet['source'].split('>')[-2].replace('</a',''),tweet['user']['followers_count'], tweet['user']['friends_count'], url, tweet['created_at'], tweet['user']['created_at'], tweet['id'],)) 
        conn.commit()
    print(screen_name, url)
    #from what source/app/device
    c.execute("select source, count(*) as cnt from tweets where screen_name like '%" + screen_name + "%' group by source order by cnt desc;")
    clients=[]
    print("Sent from: ", c.fetchall())
     
    #who are they always retweeting
    c.execute("select text from tweets where screen_name like '%" + screen_name + "%' and text like 'rt %';")
    retweeters = []
    for retweeter in c.fetchall():
        retweeters.append(str(retweeter).split(":")[0].split("@")[1])
    rt_count = Counter(retweeters)
    print("Retweets: ", rt_count.most_common(top_n))

    #IN_REPLY_TO_SCREEN_NAME
    c.execute("select in_reply_to_screen_name from tweets where screen_name like '%" + screen_name + "%';")
    reply_to_names = []
    for reply_to_name in c.fetchall():
        reply_to_names.append(reply_to_name)
    reply_to_count = Counter(reply_to_names)
    print("Replies To: ", reply_to_count.most_common(top_n))
    
    
    #who they at the most
    c.execute("select text from tweets where text not like 'rt %' and text like '%@%' and screen_name like '%" + screen_name + "%' order by tweet_id desc;")
    top_ats = []
    for phrase in c.fetchall():
        phrase = str(phrase).replace("\\n"," ")
        phrase = str(phrase)
        phrase = phrase.replace("'"," ").replace(","," ").replace("!"," ").replace(":"," ").replace("("," ").replace(")"," ").replace("/"," ")
        #print(phrase)
        words = (str(phrase).split(" "))
        for word in words:
            if '@' in word and len(word) > 1:
                top_ats.append(str(word).replace("@","").replace('"',''))
    at_count = Counter(top_ats)
    print("Initiates:", at_count.most_common(top_n))

    #schedule days
    c.execute("select tweet_at from tweets where screen_name like '%" + screen_name + "%';")
    timestamps = []

    for timestamp in c.fetchall():
        day = (str(timestamp).split(" ")[0])
        day = (str(day).split("'",)[1])    
        timestamps.append(str(day).replace(",",""))
    day_count = Counter(timestamps)
    print("Active Day: ", day_count.most_common(7))

    #schedule hours
    c.execute("select tweet_at from tweets where screen_name like '%" + screen_name + "%';")
    hourstamps = []
    for hourstamp in c.fetchall():
        hr_min_sec = (str(hourstamp).split(" ")[3])
        hour = (str(hr_min_sec).split(":")[0])
        hourstamps.append(str(hour))
    hour_count = Counter(hourstamps)
    print("Active Hr: ", hour_count.most_common(24))
    print(" ")


