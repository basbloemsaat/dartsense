from pprint import pprint
import hashlib

from dartsense import db, List_C
import dartsense.competition
import dartsense.event


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

            res = db.exec_select(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['player_name']
                self.nickname = res[0]['player_nickname']
                self.callsigns = res[0]['player_callsigns'].split(';')

    def _get_competitions(self):
        competition_list = dartsense.competition.CompetitionList(filters={'player': self.id})
        return competition_list

    competitions = property(_get_competitions)


class PlayerList(List_C):

    def __init__(self, filters={}, search=""):
        List_C.__init__(self)
        self._filters = filters
        self._searchstr = search

    def _search(self, force=False):
        if force or self._elements == []:
            self._elements = []
            args = []

            sql = '''
                SELECT DISTINCT 
                    p.player_id
                    , player_name
                    , player_nickname
                FROM player p
                    LEFT JOIN competition_player lp ON lp.player_id=p.player_id
                WHERE 
                    p.player_id > 0
            '''

            if len(self._filters) > 0:
                if 'competition' in self._filters:
                    sql += 'AND lp.competition_id=%s '
                    args.append(self._filters['competition'])

            if self._searchstr:
                sql += 'AND p.player_name LIKE %s'
                args.append('%' + self._searchstr + '%')

            res = db.exec_select(sql, args)

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
