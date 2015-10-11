#!/usr/bin/env python
"""
CLI wrapper around get_tweets and classifier.write for the 50 most populous cities in America
"""

import argparse
import datetime
import json
import mood_report

def main(cities='top_50_us.json', output='counts.csv', classifier_list=[count_dict, polar_summary]):
	now = datetime.datetime.now()
	with open(cities,'r') as f:
		cities = json.load(f)
	for city in cities:
		loc = cities[city][0]
		radius = str(int(round((cities[city][1]/3.14)**.5,0)))
		addn_query = ['geocode=' + loc + ',' + radius + 'mi']
		tweets = ' '.join(mood_report.get_tweets(now, addn_query, 10, 100))
		for classifier in classifier_list:
			data = classifier(city=city, now=now).classify(tweets)
			data.write(filepath=output)

if __name__ == '__main__':
    main()
