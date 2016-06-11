#!/usr/bin/env python
"""
Sentiment classifiers
"""

import collections
import datetime
import json
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
import os
from pkg_resources import resource_string
from textblob import TextBlob
import time


class Classifier(object):
    """MetaClass for classifier objects"""
    def __init__(self):
        self.data = {}

    __type__ = 'meta'
    now = datetime.datetime.now()
    city = 'Pythopolis'
    items = 0
    terms = 0

    def write(self, filepath):
        if not os.path.isfile(filepath):
            with open(filepath, 'w') as f:
                f.write(','.join([
                'city', 'year', 'month', 'mday', 'wday', 'hour', 'source', 'type', 'variable', 'value', 'n_items', 'n_terms'
                ]))
        for variable in self.data:
            with open(filepath, 'a') as f:
                f.write('\n' + ','.join([str(item) for item in [
                self.city,
                self.now.year,
                self.now.month,
                self.now.day,
                self.now.weekday(),
                self.now.hour,
                self.__class__,
                self.type,
                variable,
                self.data[variable],
                self.items,
                self.terms
                ]]))

class CountDict(Classifier):
    """A simple dictionary method for mood analysis"""
    def __init__(self):
        f = resource_string(__name__, 'data/emo_dict.json')
        lookup = json.loads(f.decode('utf-8'))
        self.data = {key:0 for key in lookup}
        self.lookup = lookup
        self.type = 'count'

    def classify(self, text):
        """Count number of matches for emotion categories"""
        if type(text) == str:
            text = [text]
        if type(text) == tuple:
            text = list(text)
        for item in text:
            self.items += 1
            self.terms += len(item.split(' '))
            for key in self.data:
                self.data[key] += len(set(item.lower().split()) & set(self.lookup[key]))
        return self

class PolarSummary(Classifier):
    """
    A summary of sentiment and subjectivity using pattern's classifier (via TextBlob)
    """
    def __init__(self):
        self.data = {'polarity':0, 'subjectivity':0}
        self.type = 'polarity'

    def classify(self, text):
        """Calculate sentiment summary"""
        if type(text) == str:
            text = [text]
        if type(text) == tuple:
            text = list(text)
        for item in text:
            self.items += 1
            self.terms += len(item.split(' '))
            item = TextBlob(item)
            self.data['polarity'] = self.data['polarity'] * self.items/(self.items+1) + item.sentiment.polarity / (self.items+1)
            self.data['subjectivity'] = self.data['subjectivity'] * self.items/(self.items+1) + item.sentiment.subjectivity / (self.items+1)
        return self

class WordNetDict(Classifier):
    """
    Unsupervised mood extraction using WordNet's hypernym paths
    """

    def __init__(self):
        self.data = {}
        self.type = 'count'
        self.emotion = wn.synset('emotion.n.01')

    def classify(self, text):
        """Count number/kind of emotion terms"""
        if type(text) == str:
            text = [text]
        if type(text) == tuple:
            text = list(text)
        for item in text:
            self.items += 1
            self.terms += len(item.split())
            for term in word_tokenize(item):
                for syn in wn.synsets(term):
                    for path in syn.hypernym_paths():
                        if self.emotion in path:
                            self.update_from_path(path)
        return self

    def update_from_path(self, path):
        index = path.index(self.emotion)
        try:
            self.inc(self.name_from_synset(path[index + 2]))
        except IndexError:
            self.inc(self.name_from_synset(path[index + 1]))

    def inc(self, key):
        if key in self.data:
            self.data[key] += 1
        else:
            self.data.update({key : 1})

    @staticmethod
    def name_from_synset(syn):
        return syn.name().split('.')[0]
