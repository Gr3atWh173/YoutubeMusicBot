#!/usr/bin/env python
import sys
from time import sleep
import praw
import re
import vlc
import pafy

def get_sec(tstr):
    h, m, s = tstr.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# your config shit goes here
CLIENT_ID = ''
SECRET = ''
USER_AGENT = 'Praw:YoutubeMusicBot:v0.0.1'

SUBREDDIT = sys.argv[1] if len(sys.argv) > 1 else 'metal'
TAG = sys.argv[2] if len(sys.argv) > 2 else ''

to_play_urls = []
i = vlc.Instance()
p = i.media_player_new()
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, user_agent=USER_AGENT)

print("[*] Fetching song list from reddit.com/r/{}".format(SUBREDDIT))
for s in reddit.subreddit(SUBREDDIT).hot(limit=50):
    if 'youtube.com' in s.url or 'youtu.be' in s.url:
        if TAG == '' or bool(re.search('\\[.*('+TAG+').*\\]', s.title, re.IGNORECASE)):
            to_play_urls.append(s.url)
print("[*] Fetched {} links.".format(str(len(to_play_urls))))

for url in to_play_urls:
    try:
        video = pafy.new(url)
        print("[*] Currently Playing: {}".format(str(video.title)))
        p.set_mrl(video.getbestaudio().url)
        p.play()
        sleep(get_sec(str(video.duration))+5)
    except:
        # :D
        print("[!] Skipping a video.")
