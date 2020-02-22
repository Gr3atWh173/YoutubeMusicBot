#!/usr/bin/env python

# small hack to get libvlc get working
# since just adding it to PATH on Windows doesn't work anymore
# see https://stackoverflow.com/questions/59014318/filenotfounderror-could-not-find-module-libvlc-dll
import platform
if platform.system() == 'Windows':
    import os
    os.add_dll_directory(r'C:/Program Files/VideoLAN/VLC')

import pafy
import praw
import re
import sys
import vlc

from time import sleep

# Configure your CLIENT_ID and SECRET here
CLIENT_ID = ''
SECRET = ''

USER_AGENT = 'Praw:YoutubeMusicBot:v0.0.1' 

def get_sec(tstr):
    h, m, s = tstr.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def should_append_url(submission):
    re_pattern = '\\[.*(' + TAG + ').*\\]'
    if 'youtube.com' in submission.url or 'youtu.be' in submission.url:
        if TAG == '' or bool(re.search(re_pattern, submission.title, re.IGNORECASE)):
        	return True
    return False

def fetch_urls():
    to_play_urls = []
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=SECRET, user_agent=USER_AGENT)
    print("[*] Fetching song list from reddit.com/r/{}".format(SUBREDDIT))
    for submission in reddit.subreddit(SUBREDDIT).hot(limit=50):
        if should_append_url(submission):
                to_play_urls.append(submission.url)
    print("[*] Fetched {} links.".format(str(len(to_play_urls))))
    return to_play_urls

def play_urls(urls):
    player = vlc.Instance().media_player_new()
    for url in urls:
        try:
            video = pafy.new(url)
            print("[*] Currently Playing: {}".format(str(video.title)))
            player.set_mrl(video.getbestaudio().url)
            player.play()
            sleep(get_sec(str(video.duration))+5)
        except:
            # :D
            print("[!] Skipping a video.")

def main():
    urls = fetch_urls()
    play_urls(urls)

SUBREDDIT = sys.argv[1] if len(sys.argv) > 1 else 'metal'
TAG = sys.argv[2] if len(sys.argv) > 2 else ''
main()
