#!/usr/bin/env python

setup(
    name='Mood Report',
    version='0.0.2',
    description='City-based mood tracking',
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
    keywords='spatial, emotion, classifier',
    packages=find_packages(exclude=['contrib', 'docs', '*test*']),
    install_requires=[
                    'datetime',
                    'json',
                    'os',
                    'requests_oauthlib',
                    'yaml'
                    ],
    extras_require={
        'test': ['pytest'],
    },
    package_data={
    'mood_report' = ['data/*',]
    }
)
