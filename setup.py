#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Weather Report',
    version='0.0.2',
    description='Location-based sentiment analysis',
    long_description='',
    url='',
    author='Dillon Niederhut',
    author_email='dillon.niederhut@gmail.com',
    license="BSD 2-Clause",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    requires=[
                'datetime',
                'json',
                'os',
                'requests_oauthlib',
                'yaml'
                ],
    keywords='spatial, emotion, classifier',
    packages=['Bots', 'Classifiers', 'Readers'],
    package_data={
    'weather_report' : ['data/*',]
    }
)
