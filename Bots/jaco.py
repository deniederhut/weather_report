#!/usr/bin/env python
"""
CLI wrapper around get_tweets and classifier.write
"""

import datetime
import json
import os
from weather_report import classifiers, readers
import yaml

class Jaco(object):

    def __init__(self, credsfile, key_name, secret_name, cities, output, classifier_list):
        with open(credsfile, 'r') as f:
            self.key = yaml.load(f).get(key_name)
            self.secret = yaml.load(f).get(secret_name)
        with open(cities,'r') as f:
            self.cities = json.load(f)
        self.output=output
        self.classifier_list = classifier_list

    @staticmethod
    def city_attrs(city):
        return city[0], str(int(round((city[1]/3.14)**.5,0)))

    def run(self):
        for city in self.cities:
            loc, radius = city_attrs(city)
            query = {'geocode' : loc + ',' + radius + 'mi'}
            tweetReader = Readers.tweetReader(self.key, self.secret)
            tweets = tweetReader.get(now=now, pages=50, limit=100, **query)
            for classifier in classifier_list:
                if classifier == 'count_dict':
                    data = classifiers.CountDict()
                if classifier == 'polar_summary':
                    data = classifiers.PolarSummary()
                if classifier == 'wordnet_dict':
                    data = classifiers.WordNetClassifier()
                data.now = now
                data.city = city
                data = data.classify(tweets)
                data.write(filepath=output)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('credsfile')
    parser.add_argument('key-name')
    parser.add_argument('secret-name')
    parser.add_argument('cities', type=str,
        choices=['top_50_us, top_10_us'])
    parser.add_argument('output', type=str, default='counts.csv')
    parser.add_argument('--classifiers', type=str,
        nargs='+', required=True,
        choices=['count_dict', 'polar_summary', 'wordnet_dict'])

    args = parser.parse_args()
    args.cities = os.path.join('data', args.cities + '.json')

    Jaco(**vars(args)).run()
