#!/usr/bin/python
from token_counter import TokenCounter
from fetch_comments_oauth import get_comments_text

def build_ignored_words_list():
    ignored_words = ['the', 'a', 'an', 'it', 's', 'don', 't', 'is', 'are', 'be', \
        'in', 'of', 'if', 'for', 'among', 'and', 'but', 'or', 'they', 'them', 'their',\
        'you', 'i', 'we', 'us', 'e', 'does', 'do', 'have', 'has', 'with', 'by', \
        'this', 'that', 'as', 'my', 'there', 'here', 'so', 'about', 'from', 'can', \
        'am', 'didn', 'your', 'to', 'on', 'what', 'who', 'than', 'these', 'those', \
        'all', 'some', 'also', 'too', 'not', 'since', 'each', 'every', 'most', 'own', \
        'much', 'etc', 'even', 'just', 'when', 'how', 'used', 'use', 'm', 'any', 'only',\
        'was', 'up', 'he', 'she', 'him', 'her', 'his', 'hers', 'our', 'ours', 'into', \
        'more', 'both', 'while', 'then', 'like', 'did', 'until', 'should', 'around', \
        'being', 'been', 'still', 'me', 'no', 'com', 'd', 'through', 'www', 'http', 'https']
    return ignored_words

ignored_words = build_ignored_words_list()

def count_comment_words():
    max_results = 100
    video_comments = get_comments_text(max_results=max_results)
    title = video_comments['title']
    channel = video_comments['channel']
    comments = video_comments['comments']
    ## Demo comments (avoid API quota expense while testing)
    #comments = ["first", "All the rest of these are like fake comments pretending to talk like someone ur not m8", "horses!", "horses is me. and you are not the one that is a me!!!:D", ":)", "Furrrrsst. For reals.", "horses and much Love for u", "happy with yay", "the best!", "oh wow this is sooo not for me", "Whatever. Kinda not what I thought it'd be.", "k my friend", "ur so wrong used to say rekt now it's like wut", "nice video.", "Still got it! But hey can you do one on horses?", "nope"]
    words_counter = TokenCounter()
    #words_counter.compare_tfidfs(comments)
    #words_counter.print_sorted_by_tfidf(descending=True)
    words_counter.compare_frequencies(comments)
    print("\nvideo: {0}\nchannel: {1}\n-- popular* words across {2} comments --".format(title, channel, max_results))
    words_counter.print_sorted(descending=True, use_tfidf=False, ignored_words=ignored_words, min_val=3)
