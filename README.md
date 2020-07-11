# Youtube Music Bot
### Version 2.0.0

## Changelog v2.0.0
1. Remove pafy, praw as dependencies
	- No need to register an app with reddit
	- Reduced dependencies
2. Add youtube-dl, requests
	- Now we can stream SoundCloud links as well

## What?
YoutubeMusicBot pulls down a list of youtube links from subreddits of your choosing and plays them with VLC.

## Why?
Much better than doing it myself. Besides, who doesn't like some good music while working.

## How?
0. Install VLC

1. Clone the repo
```bash
$ git clone https://github.com/Gr3atWh173/YoutubeMusicBot
```
2. Then cd into its directory and execute: 

```bash
$ pip3 install -r requirements.txt
```

You should now be ready to use YoutubeMusicBot. 
```bash
$ python bot.py usage
```

## This doesn't work for me
Open an issue or a PR.
