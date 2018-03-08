import os
import sys

import yaml

from pprint import pprint

SESSION_SECRET = os.environ['DARTSENSE_SESSION_SECRET']

database = {
    "host": os.environ['DARTSENSE_HOST'],
    "username": os.environ['DARTSENSE_USERNAME'],
    "password": os.environ['DARTSENSE_PASSWORD'],
    "schema": os.environ['DARTSENSE_SCHEMA'],
}


oauth2_file = os.path.join(os.path.dirname(__file__), "../../etc/oauth2.yaml")

pprint(oauth2_file)

with open(oauth2_file, 'r') as stream:
    try:
        pprint(yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)


