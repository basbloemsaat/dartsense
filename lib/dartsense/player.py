from pprint import pprint
import hashlib

from dartsense import db, List_C

class Player:

    def __init__(self, id=0, name='', nickname='',):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.aliases = []

class PlayerList(List_C):

    def __init__(self):
        List_C.__init__(self)

    def _search(self, force=False):
        if force or self._elements == None:
            self._elements = []

            sql = '''
                SELECT DISTINCT p.*
                FROM player p
            '''

            res = db.exec_sql(sql)

            for r in res:
                self._elements.append(Player(
                    id=r['player_id'],
                    name=r['player_name'],
                    nickname=r['player_nickname'],
                ))

    def add_player(self, player):
         self.self._elements[player.id] = player
    #     return player


    def _get_players(self):
        return self.elements
    players = property(_get_players)

   