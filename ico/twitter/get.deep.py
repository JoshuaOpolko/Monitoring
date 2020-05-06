#!/usr/bin/python3
import pymysql
from subprocess import call
import os
import tweepy 
import datetime
import time
from keys import keys

# db
db = pymysql.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
cursor = db.cursor()

# Auth
consumer_key = keys['consumer_key']
consumer_secret         = keys['consumer_secret']
access_token            = keys['access_token']
access_token_secret     = keys['access_token_secret']


#grab up to 3248 tweets per account
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

top_list = ['IoT613']

for screen_name in top_list:
    print("xxxxxxxxxxxxxxxx")
    print(screen_name)
    print("xxxxxxxxxxxxxxxx")
    alltweets = []	
    user_data = api.get_user(screen_name)
    time.sleep(2)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        time.sleep(2)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
        for tweet in alltweets:    
            try:
                if 'url' in str(user_data.entities):
                    user_url = str(tweet['user']['url'])
                else:
                    user_url = 'na'
            except:
                user_url = 'no_url_found'

            if 'profile_banner_url' not in str(user_data):
                banner = 'na'
            else:
                banner = 'user_data.profile_banner_url'
            print("url: ", str(user_data.entities['url']['urls'][0]['expanded_url']))
            cursor.execute("replace INTO twitter.tweets (tweet_id, screen_name, username, tweet_at, born, urls,symbols,description,text,followers,friends,source, location,statuses_count, time_zone, utc_offset, user_id, verified,profile_img,bg_color,banner_url,link_color, url, logged) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tweet.id,str(tweet.user.screen_name).encode("utf8","ignore"), str(tweet.user.name).encode("utf8","ignore"), tweet.created_at, user_data.created_at, str(tweet.entities['urls']).encode("utf8","ignore"),str(tweet.entities['symbols']).encode("utf8","ignore"), str(user_data.description).encode("utf8","ignore"),tweet.text.encode("utf-8"), user_data.followers_count, user_data.friends_count,tweet.source,user_data.location, str(user_data.statuses_count), user_data.time_zone, user_data.utc_offset, user_data.id, user_data.verified, user_data.profile_image_url, user_data.profile_background_color, banner,user_data.profile_link_color, str(user_data.entities['url']['urls'][0]['expanded_url']), datetime.datetime.now()))
        
        db.commit()
db.close()
print("finished")
