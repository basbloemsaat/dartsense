from flask import session, request
from pprint import pprint
from dartsense.user import User



def check_user_permission(permission):
    pprint('checking user ' + permission)

    if not 'user_id' in session:
        return False

    user = User(id = session['user_id'])

    pprint(user.permissions)

