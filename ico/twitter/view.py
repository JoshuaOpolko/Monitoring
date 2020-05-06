#!/usr/bin/python3
import pymysql
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from sys import argv
import webbrowser
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import datetime

# db
db = pymysql.connect("localhost","test","test","twitter",charset="utf8mb4",init_command='SET NAMES utf8mb4')
cursor = db.cursor()
list_of_screen_names = ['morrison']

for target_screen_name in list_of_screen_names:
    #create web page
    f = open("/home/john/tw/reports/" + target_screen_name + ".html", 'w')
    message = """<html>
    <head> <!--<meta http-equiv="refresh" content="3">--> </head>
    <body><p>clear</p></body>
    </html>"""
    f.write(message)
    f.write("\n")
    f.truncate()

    # get top ico accounts based on 24 hr retweet counts
    #get_top_rt = """select count(*) as cnt, lower(substring_index(text,':',1)) from twitter.tweets where text like '%@nct_exe%' and (tweet_at > date_sub(utc_timestamp(), interval 24 hour)) group by text order by cnt desc limit 15;"""
    get_top_rt = """select count(*) as cnt, screen_name, username, location, time_zone, description, profile_img, bg_color, banner_url, link_color, followers, friends, url, born from twitter.overnight where (username not like '%kate%perry%' and screen_name not like '%kate%perry%' and username not like '%katy%' and screen_name not like '%katy%') and username like '% """ + target_screen_name + """%' or screen_name like '% """ + target_screen_name + """%' and (tweet_at > date_sub(utc_timestamp(), interval 48 year)) group by screen_name, username, location, time_zone, description, profile_img, bg_color, banner_url, link_color, followers, friends, url, born order by cnt desc;"""
    cursor.execute(get_top_rt)
    top_rt = cursor.fetchall()
    for rt in top_rt:
        cnt = (rt[0])
        screen_name = (rt[1])
        username = (rt[2])
        location = (rt[3])
        if not location:
            location = 'noloc'     
        time_zone = (rt[4])
        description = (rt[5])
        if not description:
            description = 'nodesc'
        profile_img = (rt[6])
        bg_colour = (rt[7])
        banner_url = (rt[8])
        link_color = (rt[9])
        if not link_color:
            link_color = 'noclr'
        followers = (rt[10])
        friends = (rt[11])
        url = (rt[12])
        if not url:
            url = 'nourl'    
        born = (rt[13])
        picurl = str(profile_img).replace("_normal.",".")
        profurl = ("https://twitter.com/%s" % screen_name) 

        #print bg image
        f.write("<div style='background-color:#")
        f.write(link_color)
        f.write(";color:white;padding:10px;'><img width = 20% height = 100 src = \"")
        f.write(str(banner_url))
        f.write("\">")    
        f.write("|")
        f.write("<a href=\"")
        f.write(profurl)
        f.write("\"><img width = 100 height = 100 src = \"")
        f.write(picurl)
        f.write("\">")
        f.write("<font size = 4> </div>")
        f.write(str(cnt))
        f.write("|")
        f.write(location)    
        f.write("|")
        f.write(str(screen_name))
        f.write("|")
        f.write(str(username))
        f.write("|")
        f.write(description)
        f.write("|")
        f.write(url)
        f.write("</a></font><br>")
        f.truncate()


    #open the page in browser
    webbrowser.open_new_tab("/home/john/tw/reports/" + target_screen_name + ".html")