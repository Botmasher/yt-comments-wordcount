# YT Comment Word Counter

Parse and count words in comments left on a single YouTube video.

## Description
This tool takes a video id param for a single YouTube video, signs into the API, fetches the comments associated with the video, then works with the text of those comments.

## Getting Started
You can run this code locally without much hassle. You will need to get your own [YouTube API credentials](https://console.developers.google.com/).

1. set up your own authorization credentials in the Google Developers Console
2. save the `client_secrets.json` to the same directory as the authorization script `ytauth.py`
3. make sure you have [Python](https://www.python.org/) installed (developed with Python 3)
4. use Python to run the word count script `count_words.py`
  - pass in a `--videoid` to be read by the API fetch script: `python3 count_words.py --videoid=jNQXAC9IVRw`

## Adjusting Settings
By default the project will ask the YouTube API for 100 top-level comments. You can adjust this by changing `max_results` in main at the bottom of `count_words.py`. You can also add to or change the list of words to ignore if you're going for straight frequencies, or call the `TokenCounter` instance's `compare_tfidfs` for a smoothed result that takes into account the commonness of a word.
