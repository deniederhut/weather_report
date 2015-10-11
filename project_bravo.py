#!/usr/bin/env python
"""
Package for analyzing Twitter sentiment across the US. Defaults favor hourly CRON calls.
"""

import collections
import json
import time
import os
from textblob import TextBlob
from requests.exceptions import Timeout, ConnectionError
from requests_oauthlib import OAuth1Session

class classifier(object, city='Python', now=datetime.datetime.now()):
	"""MetaClass for classifier objects"""
	def __init__(self):
		self.data = {}
		self.type = 'meta'
		self.now = now
		self.city = city

	def write(self):
		if not os.path.isfile(filepath):
		    with open(filepath, 'w') as f:
		        f.write(','.join([
				'city', 'year', 'month', 'mday', 'wday', 'hour', 'source', 'type', 'variable', 'value'
				]))
		for variable in self.data:
			with open(filepath, 'a') as f:
				f.write(','.join([str(item) for item in [
				'\n',
				self.city,
				self.now.year,
				self.now.month,
				self.now.day,
				self.now.weekday,
				self.now.hour,
				self.__class__,
				self.type,
				variable,
				self.data[variable]
				]]))

class count_dict(classifier):
	"""A simple dictionary method for mood analysis"""
	def __init__(self):
		with open('data/emo_dict.json', 'r') as f:
			lookup = json.load(f)
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
			for key in self.data:
				self.data[key] = len(set(item.lower().split()) & set(self.lookup[key]))})
			yield self

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
			item = TextBlob(item)
			self.data['polarity'] = item.sentiment.polarity
			self.data['subjectivity'] = item.sentiment.subjectivity
			yield self

def get_tweets(now=datetime.datetime.fromtimestamp(0), addn_query = [], pages=1, limit=15):
	"""
	Gets recent en status updates from Twitter matching additional queries not older than a datetime object
	"""
	twitter = OAuth1Session(API_KEY,client_secret=API_SECRET)
	base_url = 'https://api.twitter.com/1.1/search/tweets.json'
	query_base = '?q=lang%3Aen&result_type=recent&count=' + str(limit) + '&'
	i = 0
	tweets = []
	url = base_url + query_base + '&'.join(addn_query)
	while i < pages:
		try:
			r = twitter.get(url = url)
			if r.status_code == 200:
				for status in r.json()['statuses']:
					if datetime.datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y') > (now - datetime.timedelta(1/24):
						tweets.append(status['text'])
				if r.json()['search_metadata']['next_results'] != None:
					url = base_url + r.json()['search_metadata']['next_results']
				else:
					break
			if r.status_code == 429:
				time.sleep(300)
			i += 1
		except ConnectionError:
			pass
		except Timeout:
			pass
		time.sleep(2)
	return tweets

def main(classifier_list=[count_dict, polar_summary]):
	"""
	Wrapper around get_tweets and classifier.write for the 50 most populous cities in America
	"""
	now = datetime.datetime.now()
	with open('data/cities.js','r') as f:
		cities = json.load(f)
	for city in cities:
		loc = cities[city][0]
		radius = str(int(round((cities[city][1]/3.14)**.5,0)))
		addn_query = ['geocode=' + loc + ',' + radius + 'mi']
		tweets = ' '.join(get_tweets(now, addn_query, 10, 100))
		for classifier in classifier_list:
			data = classifier(city=city, now=now).classify(tweets)
			data.write(filepath='data/counts.csv')


if __name__ == '__main__':
	main()
