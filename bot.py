#!/usr/bin/env python
# YoutubeMusicBot v0.0.1
# author: Gr3atwh173
#
# TODO: Something better that checks for when the video has ended.

import time
import time
import praw
import pafy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CLIENT_ID = 'Your client id goes here. (the thing below the name of your app)'
SECRET = 'Your secret goes here'
USER_AGENT = 'Praw:YoutubeMusicBot:v0.0.1'
SUBREDDIT = 'the music subreddit you prefer'

to_play_urls = []
to_play_names = []

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=SECRET,
                     user_agent=USER_AGENT)

print "[*] Fetching song list from reddit.com/r/{}".format(SUBREDDIT)
for s in reddit.subreddit(SUBREDDIT).hot(limit=10):
    if 'youtube.com' in s.url:
        to_play_urls.append(s.url)
        to_play_names.append(s.title)
print "[*] fetched."

print "[*] Starting firefox..."
driver = webdriver.Firefox()

i=0
while i < len(to_play_urls):
    print "[*] Currently Playing: {}".format(to_play_names[i])
    driver.get(to_play_urls[i])

    duration = pafy.new(to_play_urls[i]).duration
    time.sleep(get_sec(str(duration))+6)

    i += 1
