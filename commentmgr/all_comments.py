from urllib.request import urlopen
from urllib.request import Request
import json
from credentials import *

def fetch_all_comments(video_id=None, max_results=50):
    if video_id is None: return
    client_key = credentials['client_key']
    max_results_qparam = "" if max_results is None else "&maxResults={0}".format(max_results)
    comments_uri = "https://www.googleapis.com/youtube/v3/commentThreads?key={0}&textFormat=plainText&part=snippet&videoId={1}{2}".format(client_key, video_id, max_results_qparam)
    print(comments_uri)
    res = urlopen(Request(comments_uri))
    data = res.read()
    print("\n\n--- TOP {0} COMMENTS ---\n".format(max_results))
    for item in json.loads(data)['items']:
        print(item['snippet']['topLevelComment']['snippet']['textDisplay'])

fetch_all_comments(video_id="jNQXAC9IVRw")
