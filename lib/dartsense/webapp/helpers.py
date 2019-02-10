from flask import session, request
from dartsense.user import User

def check_user_permission(permission):
    if not 'user_id' in session:
        return False

    user_id = session['user_id']
    
    # root always has access for now
    if user_id == -1:
        return True


    user = User(id = user_id)



