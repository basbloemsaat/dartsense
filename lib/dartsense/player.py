from pprint import pprint
import hashlib

from dartsense import db, List_C



class Player:

    def __init__(self, id=0, name='', nickname='',):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.aliases = []
        self.callsigns = []

        if id and not name:
            sql = '''
                SELECT p.player_name, p.player_nickname, p.player_callsigns
                FROM player p
                WHERE p.player_id = %s 
                LIMIT 1
            '''

            res = db.exec_sql(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['player_name']
                self.nickname = res[0]['player_nickname']
                self.callsigns = res[0]['player_callsigns'].split(';')


    def _get_leagues(self):
        league_list = LeagueList(filters={'player': self.id})
        return league_list

    leagues = property(_get_leagues)



class PlayerList(List_C):

    def __init__(self, filters={}):
        List_C.__init__(self)
        self.filters = filters

    def _search(self, force=False):
        if force or self._elements == None:
            self._elements = []

            args = []

            sql = '''
                SELECT DISTINCT p.*
                FROM player p
                    JOIN league_player lp ON lp.player_id=p.player_id
                WHERE 1=1
            '''

            if len(self.filters) > 0:
                if 'league' in self.filters:
                    sql += 'AND lp.league_id=%s '
                    args.append(self.filters['league'])

            res = db.exec_sql(sql, args)

            for r in res:
                self._elements.append(Player(
                    id=r['player_id'],
                    name=r['player_name'],
                    nickname=r['player_nickname'],
                ))

    def add_player(self, player):
        self.self._elements[player.id] = player

    def _get_players(self):
        return self.elements
    players = property(_get_players)

import dartsense.league
import dartsense.event
