#!/usr/bin/python
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from ytauth import yt_authorize

# Call API captions.list method to list caption track data (no caption text)
def get_captions(youtube, video_id):
  data = youtube.captions().list(
    part="snippet",
    videoId=video_id
  ).execute()

  return data['items']

if __name__ == "__main__":
  yt = yt_authorize()
  api = yt['api']
  video_id = yt['args'].videoid

  try:
    get_captions(api, video_id)

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Finished fetching captions.")
