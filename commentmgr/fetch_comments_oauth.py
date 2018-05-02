#!/usr/bin/python
from apiclient.errors import HttpError
from ytauth import yt_authorize

# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube=None, video_id=None, max_results=20):
  if youtube is None or video_id is None: return

  results = youtube.commentThreads().list(
    part="snippet,replies",
    videoId=video_id,
    textFormat="plainText",
    maxResults=max_results
  ).execute()

  # for item in results["items"]:
  #   comment = item["snippet"]["topLevelComment"]
  #   author = comment["snippet"]["authorDisplayName"]
  #   text = comment["snippet"]["textDisplay"]
  #   print("Comment by %s: %s" % (author, text))

  print(len(results['items']))

  return results['items']


# Call the API's comments.list method to list the existing comment replies.
def get_comments(youtube, parent_id):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  # for item in results["items"]:
  #   author = item["snippet"]["authorDisplayName"]
  #   text = item["snippet"]["textDisplay"]
  #   print("Comment by %s: %s" % (author, text))

  return results["items"]

# Call externally through command line and pass a --videoid
def get_comments_text(max_results):
  yt = yt_authorize()
  api = yt['api']
  video_id = yt['args'].videoid
  try:
    video_comment_threads = get_comment_threads(youtube=api, video_id=video_id, max_results=max_results)
    #parent_id = video_comment_threads[0]["id"]
    comments_text = []
    for c in video_comment_threads:
        comments_text.append(c['snippet']['topLevelComment']['snippet']['textDisplay'])
    return comments_text

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Finished fetching comments.")
