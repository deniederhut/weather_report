#!/usr/bin/env python
"""
CLI wrapper around get_tweets and classifier.write
"""

import datetime
import json
import os
from pkg_resources import resource_string
from weather_report import classifiers, readers
import yaml

class Jaco(object):

    def __init__(self, credsfile, key_name, secret_name, cities, output, classifier_list):
        with open(credsfile, 'r') as f:
            creds = yaml.load(f)
        self.key = creds[key_name]
        self.secret = creds[secret_name]
        f = resource_string(__name__, cities)
        self.cities = json.loads(f.decode('utf-8'))
        self.output=output
        self.classifier_list = classifier_list

    @staticmethod
    def city_attrs(city):
        return city[0], str(int((float(city[1])/3.14)**.5))

    def run(self):
        now = datetime.datetime.now()
        for city in self.cities:
            loc, radius = self.city_attrs(self.cities[city])
            query = {'geocode' : loc + ',' + radius + 'mi'}
            tweetReader = readers.tweetReader(self.key, self.secret)
            tweets = tweetReader.get(now=now, pages=50, limit=100, **query)
            for classifier in self.classifier_list:
                if classifier == 'count_dict':
                    data = classifiers.CountDict()
                if classifier == 'polar_summary':
                    data = classifiers.PolarSummary()
                if classifier == 'wordnet_dict':
                    data = classifiers.WordNetDict()
                data.now = now
                data.city = city
                data = data.classify(tweets)
                data.write(filepath=self.output)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('credsfile')
    parser.add_argument('key_name')
    parser.add_argument('secret_name')
    parser.add_argument('cities', type=str,
        choices=['top_50_us', 'top_10_us'])
    parser.add_argument('output', type=str, default='counts.csv')
    parser.add_argument('classifier_list', type=str,
        nargs='+',
        choices=['count_dict', 'polar_summary', 'wordnet_dict'])

    args = parser.parse_args()
    args.cities = os.path.join('data', args.cities + '.json')

    Jaco(**vars(args)).run()
