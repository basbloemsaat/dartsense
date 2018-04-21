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


with open(os.path.join(os.path.dirname(__file__), "../../etc/oauth2.yaml"), 'r') as stream:
    try:
        oauth2 = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

remove_keys = []
for key in oauth2:
    try:
        oauth2[key]["consumer_key"] = os.environ['DARTSENSE_' + key.upper() + '_ID']
        oauth2[key]["consumer_secret"] = os.environ['DARTSENSE_' + key.upper() + '_SECRET']
    except KeyError as e:
        pprint('No oauth2 config for ' + key)
        remove_keys.append(key)


for key in remove_keys:
    oauth2.pop(key)
