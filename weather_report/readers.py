#!/usr/bin/env python
"""
Web API readers
"""

import datetime
import json
import time
from requests.exceptions import Timeout, ConnectionError
from requests_oauthlib import OAuth1Session

class tweetReader(object):
    """Gets tweets matching params with api key and secret"""

    tweets = []
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, api_key, api_secret):
        self.t = OAuth1Session(api_key,client_secret=api_secret)

    def get(self, language='en', result_type='recent', pages=1, limit=15, now=datetime.datetime.fromtimestamp(0), **kwargs):
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
