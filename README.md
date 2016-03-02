---
Title : Weather Report
Author : Dillon Niederhut
---

[![DOI](https://zenodo.org/badge/18094/deniederhut/weather_report.svg)](https://zenodo.org/badge/latestdoi/18094/deniederhut/weather_report)  [![Build Status](https://travis-ci.org/deniederhut/weather_report.svg?branch=master)](https://travis-ci.org/deniederhut/weather_report)

## Description

Weather Report is a collection of sentiment classifiers and location-based API readers. It is the engine that powers the [Berkeley Mood Twitter Bot](https://twitter.com/BerkeleyMood)<sup>1</sup>

## Installation

```
git clone https://github.com/deniederhut/weather_report.git
cd weather_report
python setup.py install
```

## Use

See `bots/jaco.py` for an example of a CLI client. Running:

```
python jaco.py top_10_us data/counts.csv --classifiers count_dict polar_summary
```

Yields:

```
head counts.csv
city,year,month,mday,wday,hour,source,type,variable,value,n_items,n_terms
Pythopolis,2016,3,2,2,11,<class 'weather_report.classifiers.CountDict'>,count,angry,0,1,12
Pythopolis,2016,3,2,2,11,<class 'weather_report.classifiers.CountDict'>,count,sad,1,1,12
Pythopolis,2016,3,2,2,11,<class 'weather_report.classifiers.CountDict'>,count,loving,1,1,12
Pythopolis,2016,3,2,2,11,<class 'weather_report.classifiers.CountDict'>,count,afraid,0,1,12
Pythopolis,2016,3,2,2,11,<class 'weather_report.classifiers.CountDict'>,count,happy,1,1,12
```

---

* 1. For more on Berkeley Mood, see the [D-Lab blog post](http://dlab.berkeley.edu/blog/berkeley-mood-twitter-and-python)
