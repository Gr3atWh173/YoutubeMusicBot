#!/usr/bin/env python3

# small hack to get libvlc to work on Windows
# this should be done before importing the vlc bindings
import platform
if platform.system() == 'Windows':
    from os import add_dll_directory
    add_dll_directory(r'C:/Program Files/VideoLAN/VLC')

from os import environ
from sys import argv
from json import loads
from random import shuffle
from time import sleep
from vlc import Instance
from requests import Session
from youtube_dl import YoutubeDL

USAGE = """
USAGE:

    python3 bot.py [subreddits] [limit]

    - Use CTRL+C to skip to next track
    - Hold CTRL+C to exit

EXAMPLES:

    python3 bot.py metal 10
    python3 bot.py listentothis+cyberpunk_music 30
"""

# constants
API_BASE = 'https://reddit.com/r/'
SUPPORTED_PROTOCOLS = ['http', 'https', 'http_dash_segments']
SUPPORTED_DOMAINS = [
    'youtube.com',
    'youtu.be',
    'soundcloud.com'
]

# initialize requests
session = Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})

# initialize youtube_dl
ytdl_opts = {
    'quiet': True,
    'format': 'bestaudio/best'
}
ytdl = YoutubeDL(ytdl_opts)

# initialize VLC 
environ["VLC_VERBOSE"] = "-1"
player = Instance('--novideo').media_player_new()

def fetch_links(subreddits: str, limit: int) -> list:
    links = []    
    raw_response = session.get(API_BASE + subreddits + '.json?limit=' + str(limit)).text
    posts = loads(raw_response)['data']['children']
    for post in posts:
        post = post['data']
        if post['selftext'] != '': continue
        if not post['domain'] in SUPPORTED_DOMAINS: continue
        if 'playlist' in post['url']: continue
        links.append(post['url']) 

    shuffle(links)
    return links

def select_stream(streams: dict) -> str:
    streams = [stream['url'] for stream in streams if stream['protocol'] in SUPPORTED_PROTOCOLS]
    # FUTURE: select the best audio quality
    return streams[0]
    
def extract_info(link: str) -> tuple:
    info = ytdl.extract_info(link, download=False)
    mrl = select_stream(info['formats'])
    return (mrl, info['title'], info['duration'])

def play(link: str):
    mrl, name, duration = extract_info(link)
    
    print("[*] Now Playing: {}".format(name))
    player.set_mrl(mrl, ":no-video")
    player.play()
    # wait for song to finish playing
    sleep(duration+2)

def main(subreddits: str = 'listentothis', limit: int = 40):
    print("[*] Fetching links from {}...".format(subreddits))
    links = fetch_links(subreddits, limit)
    print("[*] Fetched {} links".format(len(links)))
    
    for link in links:
        try:
            play(link)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    if len(argv) == 2 and argv[1].lower() == 'usage':
        print(USAGE)
    else:
        subreddits = argv[1]
        limit = 40
        if len(argv) == 3: limit = int(argv[2])
        main(subreddits, limit)
