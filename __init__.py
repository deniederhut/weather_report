#!/usr/bin/env python

import os
import yaml

with open(os.path.join(os.getenv('HOME'), 'creds.yml')) as f:
    creds = yaml.load(f)
API_KEY = creds['bravo-key']
API_SECRET = creds['bravo-secret']
