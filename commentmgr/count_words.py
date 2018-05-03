#!/usr/bin/python
import operator
import re
from fetch_comments_oauth import get_comments_text

class TokenCounter:
    def __init__ (self):
        self.texts_per_word = {}

    def unique_words(self, text):
        text = text.lower()
        words = re.compile(r'\W+', re.UNICODE).split(text)
        word_counts = { word : self.texts_per_word[word] + 1 if word in self.texts_per_word.keys() else 1 for word in words }
        if '' in word_counts.keys(): word_counts.pop('', None)
        self.texts_per_word = {**self.texts_per_word, **word_counts}
        return

    def print_sorted_unique_words(self, descending=False):
        sorted_word_count_pairs = sorted(self.texts_per_word.items(), key=operator.itemgetter(1), reverse=descending)
        for word_count in sorted_word_count_pairs:
            print(word_count)
        return

if __name__ == "__main__":
    comments = get_comments_text(max_results=100)
    words_counter = TokenCounter()
    for comment in comments:
        words_counter.unique_words(comment)
    words_counter.print_sorted_unique_words(descending=True)
