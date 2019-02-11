from pprint import pprint
import hashlib

from dartsense import db


class User:

    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self._name = name
        self._email = email

        if self.id and not self._name:
            sql = '''
                SELECT 
                    user_name, user_email
                FROM user 
                WHERE user_id=%s 
                LIMIT 1 
                '''
            try:
                res = db.exec_select(sql, [
                    self.id,
                ])[0]

                self._name = res['user_name']
                self._email = res['user_email']

            except (IndexError) as e:
                pass

    def _get_permissions(self):
        return []

    def login(self, provider=None, credential=None):
        if self.id:
            return False

        sql = '''
            SELECT 
                user_id
            FROM usercredential
            WHERE usercred_provider=%s and usercred_value=%s
            LIMIT 1 
            '''

        try:
            res = db.exec_select(sql, [
                provider, credential
            ])[0]

            self.__init__(res['user_id'])

        except (IndexError) as e:
            return False

        return True

    def _get_name(self):
        return self._name

    def _get_email(self):
        return self._email

    name = property(_get_name)
    email = property(_get_email)
    permissions = property(_get_permissions)
