from flask import session, request
from pprint import pprint
from dartsense.user import User



def check_user_permission(permission):
    # pprint('checking user ' + permission)

    if not 'user_id' in session:
        pprint('no user_id')
        return False

    user_id = session['user_id']
    # pprint(user_id)
    
    # root always has access for now
    if user_id == -1:
        return True


    user = User(id = user_id)



