# YT Comment Word Counter

YouTube projects for reading, monitoring and analyzing bulk account data. Began as one tool to parse and count words in comments left on a single YouTube video.

## Description
This tool takes a video id param for a single YouTube video, signs into the API, fetches the comments associated with the video, then works with the text of those comments.

## Getting Started
Here are some steps you can take to run this code locally. You will need to have your own [YouTube API credentials](https://console.developers.google.com/).

1. set up your own authorization credentials in the Google Developers Console
2. save the `client_secrets.json` to the same directory as the authorization script `ytauth.py`
3. make sure you have [Python](https://www.python.org/) installed (developed with Python 3)
4. get a copy of this project
5. navigate to the project directory on your local machine
6. use `pip` to install the package: `pip3 install . --upgrade`
7. use `python` to run the package: `python3 yt_comments_wordcount`
  - hook up the comments count script to `main` then pass a video: `--videoid=jNQXAC9IVRw`
  - hook up the captions script in `main` then pass a channel:
  `--channelid=YT_CHANNEL_ID`

The OAuth flow may cause the application to log a URL to the terminal. If so, follow these steps:
8. open a browser and visit URL logged in the terminal
9. sign into a YouTube account
10. agree to allow the app to read your account data
11. copy the authorization code given in the browser
12. paste the authorization code in the terminal

The application should now be running the code starting in `main.py`.

## Captions Subproject
_TODO: update this README to cover these YouTube API miniprojects more broadly._

Fetch caption tracks across videos and look for ones with specific properties. The current implementation searches for language captions that are drafts held in review across all videos.

## Comments Subproject
Parse and count words in comments left on a single YouTube video. By default the project will ask the YouTube API for 100 top-level comments. You can adjust this by changing `max_results` in the main function at the bottom of `count_words.py`. You can also add to or change the list of words to ignore if you're going for straight frequencies, or call the `TokenCounter` instance's `compare_tfidfs` method for a smoothed result that takes into account the commonness of a word.
