from fetch_captions_oauth import get_caption_languages

# Read captions data snippets looking for drafts

# TODO: split this and fetch_captions api calls into new project

def print_channel_draft_captions():
    """Find and print channel language captions that have drafts in review"""
    # fetch captions snippets for all videos
    max_results = 200
    captions_data = get_caption_languages(max_results)

    # collect video titles and lists of draft caption languages 
    draft_captions = {
        video_data['title']: [
            caption['language'] for caption in video_data['captions']
            if caption['isDraft']
        ]
        for video_data in captions_data.values()
    }

    # # optionally remove data with empty draft captions list 
    # { title: languages for title,languages in draft_captions.items() if languages }

    # log video titles and languages for draft captions
    for title, languages in draft_captions.items():
        print("Video title: ", title)
        print("Draft languages: ", languages)

    return draft_captions
