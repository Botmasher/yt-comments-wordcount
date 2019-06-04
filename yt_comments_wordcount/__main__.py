#from count_words import count_comment_words
from channel_draft_captions import print_channel_draft_captions
from ytauth_oauth import yt
import argparse

def main():
	print("Running")

	# Get yt api
	youtube = yt()
	
	# Parse command line args
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--channel", "--c",
		help="a single YouTube channel id"
	)
	parser.add_argument(
		"--video", "--id",
		help="a single YouTube video id"
	)
	args = parser.parse_args()

	# Run specific tasks

	#video = args.video if args.video else args.v
	#count_comment_words(youtube, video)

	channel = args.channel if args.channel else args.c
	print_channel_draft_captions(
		youtube, 		# YT Data API v3
		channel,		# Valid channel id
		max_results=50 	# Values must be within the range: [0, 50]
	)
	
	return

if __name__ == '__main__':
	main()
