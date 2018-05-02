#!/usr/bin/python
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from ytauth import yt_authorize

# Call API captions.list method to list caption track data (no caption text)
def get_captions(youtube, video_id, language='en'):
  data = youtube.captions().list(
    part="snippet",
    videoId=video_id
  ).execute()

  captions_id = None
  for item in data['items']:
    if item['snippet']['trackKind'] == 'standard' and item['snippet']['language'] == language:
      captions_id = item['id']
      break

  return captions_id

# Call API captions.download method to download the captions text for one track
def download_captions(youtube, track_id):
  data = youtube.captions().download(
    id=track_id
  ).execute()

  return track_id

if __name__ == "__main__":
  yt = yt_authorize()
  api = yt['api']
  video_id = yt['args'].videoid

  try:
    caps_id = get_captions(api, video_id)
    download_captions(api, caps_id)

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Finished fetching captions.")
