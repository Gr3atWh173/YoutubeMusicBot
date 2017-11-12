#!/usr/bin/env python
# YoutubeMusicBot v0.1.0
# author: Gr3atwh173

import sys
import time
import praw
import vlc
import pafy

def get_sec(tstr):
    h, m, s = tstr.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)
    
CLIENT_ID = 'your client id goes here'
SECRET = 'your app secret goes here'
USER_AGENT = 'Praw:YoutubeMusicBot:v0.0.1'
try:
    SUBREDDIT = sys.argv[1] if sys.argv[1] else 'metal'
except:
    SUBREDDIT = 'metal'

to_play_urls = []
i = vlc.Instance()
p = i.media_player_new()
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, user_agent=USER_AGENT)

print("[*] Fetching song list from reddit.com/r/{}".format(SUBREDDIT))
for s in reddit.subreddit(SUBREDDIT).hot(limit=50):
    if 'youtube.com' in s.url or 'youtu.be' in s.url:
        to_play_urls.append(s.url)
print("[*] Fetched {} links.".format(str(len(to_play_urls))))

for url in to_play_urls:
    try:
        video = pafy.new(url)
        print("[*] Currently Playing: {}".format(str(video.title)))
        p.set_mrl(video.getbestaudio().url)
        p.play()
        time.sleep(get_sec(str(video.duration))+10)
    except KeyboardInterrupt:
        break
    except:
        print("[!] Skipping a video.")
