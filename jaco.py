#!/usr/bin/env python
"""
CLI wrapper around get_tweets and classifier.write
"""

import argparse
import datetime
import json
import mood_report
import os

parser = argparse.ArgumentParser()
parser.add_argument('cities', type=str, choices=['top_50_us'])
parser.add_argument('output', type=str, default='counts.csv')
parser.add_argument('--classifiers', type=str, nargs='+', required=True, choices=['count_dict', 'polar_summary'])
args = parser.parse_args()
args.cities = os.path.join('data', args.cities + '.json')


def main(cities='top_50_us.json', output='counts.csv', classifier_list=['count_dict', 'polar_summary']):
	now = datetime.datetime.now()
	with open(cities,'r') as f:
		cities = json.load(f)
	for city in cities:
		loc = cities[city][0]
		radius = str(int(round((cities[city][1]/3.14)**.5,0)))
		addn_query = ['geocode=' + loc + ',' + radius + 'mi']
		tweets = ' '.join(mood_report.get_tweets(now, addn_query, 10, 100))
		for classifier in classifier_list:
			data = classifier()
			data.now = now
			data.city = city
			data = data.classify(tweets)
			data.write(filepath=output)

if __name__ == '__main__':
    main(
    cities=args.cities,
    output=args.output,
    classifier_list=args.classifiers
    )
