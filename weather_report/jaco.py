#!/usr/bin/env python
"""
CLI wrapper around get_tweets and classifier.write
"""

import datetime
import json
import os
import weather_report
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
            tweetReader = weather_report.tweetReader(self.key, self.secret)
    		tweets = tweetReader.get(now=now, pages=50, limit=100, **query)
    		for classifier in classifier_list:
    			if classifier == 'count_dict':
    				data = weather_report.count_dict()
    			if classifier == 'polar_summary':
    				data = weather_report.polar_summary()
    			data.now = now
    			data.city = city
    			data = data.classify(tweets)
    			data.write(filepath=output)

def main(cities='top_50_us.json', output='counts.csv', classifier_list=['count_dict', 'polar_summary']):
	now = datetime.datetime.now() - datetime.timedelta(1/24)



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
        choices=['count_dict', 'polar_summary'])

    args = parser.parse_args()
    args.cities = os.path.join('data', args.cities + '.json')

    Jaco(**vars(args)).run()
