from pprint import pprint
import hashlib

from dartsense import db


class User:

    def __init__(self, id=0):
        self.id = id

    def get_permissions(self):
        return []

