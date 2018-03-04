import os
import sys

SESSION_SECRET = os.environ['DARTSENSE_SESSION_SECRET']

database = {
    "host": os.environ['DARTSENSE_HOST'],
    "username": os.environ['DARTSENSE_USERNAME'],
    "password": os.environ['DARTSENSE_PASSWORD'],
    "schema": os.environ['DARTSENSE_SCHEMA'],
}



