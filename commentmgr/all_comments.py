from urllib.request import urlopen
from urllib.request import Request
import json
from credentials import *

def get_client_key():
    return credentials['client_key']

def fetch_all_comments(video_id=None, max_results=None):
    if video_id is None: return
    client_key = get_client_key()
    max_results_qparam = "" if max_results is None else "&maxResults={0}".format(max_results)
    comments_uri = "https://www.googleapis.com/youtube/v3/commentThreads?key={0}&textFormat=plainText&part=snippet&videoId={1}{2}".format(client_key, video_id, max_results_qparam)
    res = urlopen(Request(comments_uri))
    data = res.read()
    print("\n\n--- TOP {0} COMMENTS ---\n".format(max_results))
    for item in json.loads(data)['items']:
        print(item['snippet']['topLevelComment']['snippet']['textDisplay'])

def fetch_video_title(video_id=None):
    if video_id is None: return
    client_key = get_client_key()
    video_uri = "https://www.googleapis.com/youtube/v3/videos?key={0}&part=snippet&id={1}".format(client_key, video_id)
    data = urlopen(video_uri).read()
    return json.loads(data)['items'][0]['snippet']['title']

vid = "jNQXAC9IVRw"
fetch_all_comments(video_id=vid, max_results=100)
print("\n(Above comments for \"" + fetch_video_title(video_id=vid) + "\")\n")
