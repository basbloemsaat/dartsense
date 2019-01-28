from flask import session, request
from pprint import pprint
from dartsense.user import User



def check_user(permission):
    pprint('checking user ' + permission)
