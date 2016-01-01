#!/usr/bin/env python
"""
Package for analyzing Twitter sentiment across the US. Defaults favor hourly CRON calls.
"""

import collections
import datetime
import json
import time
import os
from pkg_resources import resource_string
from textblob import TextBlob
from requests.exceptions import Timeout, ConnectionError
from requests_oauthlib import OAuth1Session

class classifier(object):
    """MetaClass for classifier objects"""
    def __init__(self):
        self.data = {}

    __type__ = 'meta'
    now = datetime.datetime.now()
    city = 'Python'
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
                self.data[key] = len(set(item.lower().split()) & set(self.lookup[key]))
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
            self.data['polarity'] = item.sentiment.polarity
            self.data['subjectivity'] = item.sentiment.subjectivity
        return self

class tweetReader(object):
    """Gets tweets matching params with api key and secret"""

    tweets = []
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, api_key, api_secret):
        self.t = OAuth1Session(api_key,client_secret=api_secret)

    def get(self, lang='en', result_type='recent', pages=1, limit=15, now=datetime.datetime.fromtimestamp(0), **kwargs):
        """
        Gets recent status updates from Twitter matching
        additional queries not older than a datetime object
        """
        search_url = self.base_url + '?q=lang%3A{}&result_type={}&count={}'.format(language, result_type, str(limit))
        if kwargs:
            search_url += '&' + '&'.join(['='.join(item) for item in kwargs.items()])
        i = 0
        while i < pages:
            try:
                r = self.t.get(url=search_url)
                if r.status_code == 200:
                    for status in r.json()['statuses']:
                        if datetime.datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > now:
                            self.tweets.append(status['text'])
                    if 'next_results' in r.json()['search_metadata']:
                        search_url = self.base_url + r.json()['search_metadata']['next_results']
                    else:
                        break
                if r.status_code == 429:
                    time.sleep(60)
                i += 1
            except ConnectionError:
                pass
            except Timeout:
                pass
            time.sleep(2)
        return self.tweets
