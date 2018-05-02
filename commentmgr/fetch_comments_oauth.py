#!/usr/bin/python
from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from ytauth import yt_authorize

# Call the API's commentThreads.list method to list the existing comment threads.
def get_comment_threads(youtube, video_id):
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    textFormat="plainText"
  ).execute()

  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    print("Comment by %s: %s" % (author, text))

  print(len(results["items"]))

  return results["items"]


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


# Call the API's comments.insert method to reply to a comment.
# (If the intention is to create a new to-level comment, commentThreads.insert
# method should be used instead.)
def insert_comment(youtube, parent_id, text):
  insert_result = youtube.comments().insert(
    part="snippet",
    body=dict(
      snippet=dict(
        parentId=parent_id,
        textOriginal=text
      )
    )
  ).execute()

  author = insert_result["snippet"]["authorDisplayName"]
  text = insert_result["snippet"]["textDisplay"]
  print("Replied to a comment for %s: %s" % (author, text))


# Call the API's comments.update method to update an existing comment.
def update_comment(youtube, comment):
  comment["snippet"]["textOriginal"] = 'updated'
  update_result = youtube.comments().update(
    part="snippet",
    body=comment
  ).execute()

  author = update_result["snippet"]["authorDisplayName"]
  text = update_result["snippet"]["textDisplay"]
  print("Updated comment for %s: %s" % (author, text))


# Call the API's comments.setModerationStatus method to set moderation status of an
# existing comment.
def set_moderation_status(youtube, comment):
  youtube.comments().setModerationStatus(
    id=comment["id"],
    moderationStatus="published"
  ).execute()

  print("%s moderated succesfully" % comment["id"])


# Call the API's comments.markAsSpam method to mark an existing comment as spam.
def mark_as_spam(youtube, comment):
  youtube.comments().markAsSpam(
    id=comment["id"]
  ).execute()

  print("%s marked as spam succesfully" % comment["id"])


# Call the API's comments.delete method to delete an existing comment.
def delete_comment(youtube, comment):
  youtube.comments().delete(
    id=comment["id"]
  ).execute()

  print("%s deleted succesfully" % comment["id"])


if __name__ == "__main__":
  yt = yt_authorize()
  api = yt['api']
  video_id = yt['args'].videoid
  try:
    video_comment_threads = get_comment_threads(api, video_id)
    print(video_comment_threads)
    #parent_id = video_comment_threads[0]["id"]
    #insert_comment(youtube, parent_id, args.text)
    #update_comment(youtube, video_comments[0])
    #set_moderation_status(youtube, video_comments[0])
    #mark_as_spam(youtube, video_comments[0])
    #delete_comment(youtube, video_comments[0])

  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("Inserted, listed, updated, moderated, marked and deleted comments.")
