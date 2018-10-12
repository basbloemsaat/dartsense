import os
import sys
import yaml


from pprint import pprint

if 'DARTSENSE_SESSION_SECRET' in os.environ:
    SESSION_SECRET = os.environ['DARTSENSE_SESSION_SECRET']
elif os.environ['DARTSENSE_ENV'] == 'DEV' or os.environ['DARTSENSE_ENV'] == 'TEST':
    SESSION_SECRET = 'DEADBEEF'
    print("WARNING: Session secret not secure")
else:
    raise os.environ['DARTSENSE_SESSION_SECRET']

if 'DARTSENSE_HOST' in os.environ and 'DARTSENSE_USERNAME' in os.environ and 'DARTSENSE_PASSWORD' in os.environ and 'DARTSENSE_SCHEMA' in os.environ:

    database = {
        "type": 'mysql',
        "host": os.environ['DARTSENSE_HOST'],
        "username": os.environ['DARTSENSE_USERNAME'],
        "password": os.environ['DARTSENSE_PASSWORD'],
        "schema": os.environ['DARTSENSE_SCHEMA'],
    }
    session_type=''

elif os.environ['DARTSENSE_ENV'] == 'DEV' or os.environ['DARTSENSE_ENV'] == 'TEST':
    database = {
        "type": 'sqlite3',
        "file": 'dev/dev.sqlite3',
        "host": None,
        "username": None,
        "password": None,
        "schema": None,
    }
    session_type = 'dev'
    print("WARNING: Using development db")

with open(os.path.join(os.path.dirname(__file__), "../../etc/oauth2.yaml"), 'r') as stream:
    try:
        oauth2 = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

remove_keys = []
for key in oauth2:
    try:
        oauth2[key]["consumer_key"] = os.environ[
            'DARTSENSE_' + key.upper() + '_ID']
        oauth2[key]["consumer_secret"] = os.environ[
            'DARTSENSE_' + key.upper() + '_SECRET']
    except KeyError as e:
        pprint('No oauth2 config for ' + key)
        remove_keys.append(key)

removed_keys = {}
for key in remove_keys:
    removed_keys[key] = oauth2.pop(key)

if not 'google' in oauth2 and os.environ['DARTSENSE_ENV'] == 'DEV' or os.environ['DARTSENSE_ENV'] == 'TEST':
    oauth2['google'] = removed_keys['google']
    oauth2['google']['consumer_key']= 'test'
    oauth2['google']['consumer_secret']= '12378127349734597012497'

    print("WARNING: oauth2 development crap credentials used")

