#!/usr/bin/python
from fetch_comments_oauth import get_comments_text

def count_word_frequencies(text):
    return None

if __name__ == "__main__":
    comments = get_comments_text(max_results=50)
    print(comments)
