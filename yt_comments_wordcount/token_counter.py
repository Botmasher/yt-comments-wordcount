#!/usr/bin/python
import operator
import re
from math import log

# TODO account for the same author posting the same comment multiple times

class TokenCounter:
    def __init__(self):
        self.texts_per_word = {}
        self.tf_idfs = {}

    def split_text(self, raw):
        """Divide a string of raw text into an array of words"""
        text = raw.lower()
        words = re.compile(r'\W+', re.UNICODE).split(text)
        return words

    def term_frequency(self, words):
        """Calculate the frequency of each word in a list smoothed by count of words in the list"""
        tfs = {}
        # get the raw count of words in a text
        for word in words:
            if word: tfs[word] = tfs[word]+1 if word in tfs.keys() else 1
            # TODO unpack then pack by len(words) factor when storing word count to avoid reloop
        for word in tfs.keys():
            tfs[word] = tfs[word] / len(words)
        return

    def print_sorted(self, descending=False, use_tfidf=False, ignored_words=[], min_val=0):
        """Sort, format and print the stored frequency calculations per word"""
        word_counts_map = self.texts_per_word.items() if not use_tfidf else self.tf_idfs.items()
        sorted_pairs = sorted(word_counts_map, key=operator.itemgetter(1), reverse=descending)
        for word_count in sorted_pairs:
            word, count = word_count
            if word not in ignored_words and count >= min_val:
                print("{0}: {1}".format(word, count))
        return

    def document_frequency(self, documents):
        """Count the number of documents in which each token occurs"""
        frequencies = {}
        for document in documents:
            # tally unique words
            words = set(self.split_text(document))
            for word in words:
                if word: frequencies[word] = frequencies[word] + 1 if word in frequencies else 1
        return frequencies

    def compare_frequencies(self, texts):
        """Count and store the number of texts in which each word appears"""
        frequencies = self.document_frequency(texts)
        self.texts_per_word = frequencies
        return

    def compare_tfidfs(self, texts):
        """Calculate average tf-idf weights for words across a list of texts"""
        dfs = self.document_frequency(texts)
        tfs = {}

        # tally term frequencies weighted by document lengths
        for document in texts:
            words = self.split_text(document)
            for word in words:
                if word and word not in tfs.keys(): tfs[word] = []
                word and tfs[word].append(1 / len(words))

        # average tf idfs for each term across all documents
        tf_idfs = {term: sum(tfs[term]) / len(texts) * log(len(texts) / dfs[term]) for term in tfs}

        self.tf_idfs = tf_idfs
        return
