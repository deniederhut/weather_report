#!/usr/bin/env python
"""
Sentiment classifiers
"""

import collections
import datetime
import json
import time
import os
from pkg_resources import resource_string
from textblob import TextBlob


class classifier(object):
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

class count_dict(classifier):
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

class polar_summary(classifier):
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
