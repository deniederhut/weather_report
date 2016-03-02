#!/usr/bin/env python

from datetime import datetime
import os
import pytest
from weather_report import classifiers

filename = 'write_test.csv'

def test_metaclass():
    classifier = classifiers.Classifier()
    assert classifier.city == 'Pythopolis'
    assert classifier.now <= datetime.now()

def test_count_dict():
    classifier = classifiers.CountDict()
    classifier.classify("I love how happy it makes you to see them being sad")
    assert classifier.data == {'afraid': 0, 'angry': 0, 'happy': 1, 'loving': 1, 'sad': 1}
    assert classifier.items == 1
    classifier.write(filename)
    assert os.path.isfile(filename)
    with open(filename, 'r') as f:
        data = f.read()
    assert data.split('\n')[0] == 'city,year,month,mday,wday,hour,source,type,variable,value,n_items,n_terms'
    assert data.split('\n')[4]
    os.remove(filename)

def test_polar_summary():
    classifier = classifiers.PolarSummary()
    classifier.classify('I am so sad, I am so very very sad')
    assert classifier.data == {'polarity': -0.2875, 'subjectivity': 0.5}
    classifier.classify("And they lived happily ever after")
    assert classifier.items == 2
    assert classifier.data == {'polarity': 0.07500000000000001, 'subjectivity': 0.6666666666666666}
