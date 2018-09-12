# Youtube Music Bot
### Version 0.0.1

## What?
YoutubeMusicBot pulls down a list of youtube links from a 
subreddit of your choosing and plays their audio.

## Why?
Much better than doing it myself. Besides, who doesn't like
some good music while programming.

## How?
1. First, clone the repo
```bash
$ git clone https://github.com/Gr3atWh173/YoutubeMusicBot
```
2. Then cd into its directory and execute: 

```bash
$ pip install -r requirements.txt
```
3. Now [register an app with reddit](https://ssl.reddit.com/prefs/apps/) <br>

4. Update ```bot.py``` with your API details

You should now be ready to use YoutubeMusicBot.

5. Provide YoutubeMusicBot with the subreddit name: 

```bash
$ python bot.py music_subreddit
```
 You could also limit the search results to the ones, containing a specific tag:

```bash
$ python bot.py music_subreddit tag
```
## Requirements
<ol>
  <li> VLC Player version 2.2.X </li>
</ol>

## This doesn't work for me
Open an issue or a PR.