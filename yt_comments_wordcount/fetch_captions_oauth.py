#!/usr/bin/python
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from ytauth import yt_authorize

# TODO: compare captions across all videos
# Look for transcriptions being held "in review"
# (The transcriptions page on yt studio ui has translations
# for both title/desc and the captions alongside each other)

# - fetch all videos (? API Search: list)
# - create dict of video ids to video titles, captions
#   {
#     'id_0': {
#       'title': 'video title 0',
#       'languages': []
#     }
#   }
# - read captions on each video (API Captions: list)
# - determine which captions are in review
# - add unreviewed languages to the languages list
# - pop ids from dict where languages list is empty
# - option to download caption track (API Captions: download)

def list_video_draft_caption_languages(youtube, video_id=""):
  """List languages with draft captions in review for one video"""
  # fetch transcriptions metadata
  captions_data = youtube.captions().list(
    part = "snippet",
    videoId = video_id
  ).execute()
  # record any draft captions
  drafts = list(filter(
    lambda caption: caption['snippet']['isDraft'],
    captions_data['items']
  ))
  # create and return a list of draft caption languages
  draft_languages = [draft['language'] for draft in drafts]
  return draft_languages

def list_channel_draft_caption_languages(youtube, channel="", max_results=100):
  """Search channel videos for draft captions and return a list of data with
  video ids, titles and languages with captions in review."""

  # fetch data for all channel videos up to max results
  videos_data = youtube.search().list(
    part = "snippet",
    #forMine = True,
    channelId = "UCMk_WSPy3EE16aK5HLzCJzw",
    maxResults = max_results,
    q = "*",
    type = "video"
  ).execute()

  # create a list of id, title pairs for videos
  video_ids_titles = list(map(
    lambda video: (
      video['items']['id']['videoId'],
      video['items']['snippet']['title']
    ),
    videos_data
  ))

  # search video ids for draft captions
  draft_captions_per_video = {}
  for video_id, video_title in video_ids_titles:
    draft_languages = list_video_draft_caption_languages(youtube, video_id)
    # store draft languages in video captions dict
    if draft_languages:
      draft_captions_per_video[video_id] = {
        'id': video_id,
        'title': video_title,
        'drafts': draft_languages
      }
    
  # send back any found drafts in review
  return draft_captions_per_video
  
# NOTE: example caption data for one video
# - verify that isDraft is the relevant setting
# {
#  "kind": "youtube#captionListResponse",
#  "etag": "\"XpPGQXPnxQJhLgs6enD_n8JR4Qk/6Q8h_jC1y5GowjqL1_JaADW_Cks\"",
#  "items": [
#   {
#    "kind": "youtube#caption",
#    "etag": "\"XpPGQXPnxQJhLgs6enD_n8JR4Qk/FyBkzc2A3bD1javF5lel4U7Q6RA\"",
#    "id": "re8tPPF5JuYkgIYVk4e2tIxgMxQgonwSUV_-ScxxrPU=",
#    "snippet": {
#     "videoId": "G-GQRYA_yMw",
#     "lastUpdated": "2019-05-14T21:37:09.761Z",
#     "trackKind": "ASR",
#     "language": "en",
#     "name": "",
#     "audioTrackType": "unknown",
#     "isCC": false,
#     "isLarge": false,
#     "isEasyReader": false,
#     "isDraft": false,
#     "isAutoSynced": false,
#     "status": "serving"
#    }
#   },
#   {
#    "kind": "youtube#caption",
#    "etag": "\"XpPGQXPnxQJhLgs6enD_n8JR4Qk/o7YiOQ5OA_bQuYUW8SS5P1X6-7s\"",
#    "id": "VkDJXR4GXEv2o1YsWgZ2qPow-4typS6p",
#    "snippet": {
#     "videoId": "G-GQRYA_yMw",
#     "lastUpdated": "2019-05-14T23:59:24.785Z",
#     "trackKind": "standard",
#     "language": "en",
#     "name": "",
#     "audioTrackType": "unknown",
#     "isCC": false,
#     "isLarge": false,
#     "isEasyReader": false,
#     "isDraft": false,
#     "isAutoSynced": false,
#     "status": "serving"
#    }
#   },
#   {
#    "kind": "youtube#caption",
#    "etag": "\"XpPGQXPnxQJhLgs6enD_n8JR4Qk/BE9CjJjcqA-7Q7HXy2eWQShDHYk\"",
#    "id": "VkDJXR4GXEsqcJvxSgsXr_hO6FbIw9ix",
#    "snippet": {
#     "videoId": "G-GQRYA_yMw",
#     "lastUpdated": "2019-05-20T04:56:37.512Z",
#     "trackKind": "standard",
#     "language": "pt",
#     "name": "",
#     "audioTrackType": "unknown",
#     "isCC": false,
#     "isLarge": false,
#     "isEasyReader": false,
#     "isDraft": false,
#     "isAutoSynced": false,
#     "status": "serving"
#    }
#   }
#  ]
# }

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

  return data

def write_file(data):
    with open("captions.txt", "w") as file:
        file.write(data)
    return

if __name__ == "__main__":
  yt = yt_authorize()
  api = yt['api']
  video_id = yt['args'].videoid

  try:
    caps_id = get_captions(api, video_id)
    caps = download_captions(api, caps_id).decode("utf-8")
    write_file(caps)

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Finished fetching captions.")
