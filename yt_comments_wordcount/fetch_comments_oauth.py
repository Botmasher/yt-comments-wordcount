#!/usr/bin/python
from apiclient.errors import HttpError
#from ytauth import yt_authorize_one_video

# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube=None, video_id=None, max_results=20):
	"""Fetch comment threads on a single video"""
	if not youtube or not video_id: return
	results = youtube.commentThreads().list(
		part="snippet,replies",
		videoId=video_id,
		textFormat="plainText",
		maxResults=max_results
	).execute()

	return results['items']

def get_comments(youtube=None, parent_id=None):
	"""Fetch replies to a single comment"""
	if not youtube or parent_id is None: return

	results = youtube.comments().list(
		part="snippet",
		parentId=parent_id,
		textFormat="plainText"
	).execute()

	return results['items']

def get_video(youtube=None, video_id=None):
	"""Fetch details for a single video"""
	if not youtube or not video_id: return

	results = youtube.videos().list(
		part="snippet",
		id=video_id
	).execute()

	return results['items'][0]['snippet']

def get_channel(youtube=None, channel_id=None):
	"""Fetch details of a single channel"""
	if not youtube or not channel_id: return

	results = youtube.channels().list(
		part="snippet",
		id=channel_id
	).execute()

	return results['items'][0]['snippet']

# TODO: update to use current oauth and app flow
# Call externally through command line and pass a --videoid
def get_comments_text(max_results):
	yt = yt_authorize_one_video()
	api = yt['api']
	video_id = yt['args'].videoid if yt['args'].videoid else yt['args'].v
	try:
		video_comment_threads = get_comment_threads(youtube=api, video_id=video_id, max_results=max_results)
		#parent_id = video_comment_threads[0]["id"]
		video = get_video(youtube=api, video_id=video_id)
		video_title = video['title']
		channel = get_channel(youtube=api, channel_id=video['channelId'])
		channel_title = channel['title']
		comments_text = []
		for c in video_comment_threads:
			comments_text.append(c['snippet']['topLevelComment']['snippet']['textDisplay'])
		return {'title': video_title, 'channel': channel_title, 'comments': comments_text}

	except HttpError as e:
		print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
	else:
		print("Finished fetching comments.")
