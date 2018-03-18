from pprint import pprint
from dartsense import List_C
from dartsense import db
from dartsense.player import PlayerList


class League:

    def __init__(self, id=0, name='',):
        self.id = id
        self.name = name

        if id and not name:
            sql = "SELECT league_id, league_name FROM league where league_id=%s LIMIT 1"
            res = db.exec_sql(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['league_name']

    def _get_players(self):
        player_list = PlayerList(filters={'league': self.id})
        return player_list

    players = property(_get_players)


class LeagueList(List_C):

    def __init__(self):
        List_C.__init__(self)

    def _search(self, force=False):
        if force or self._elements == None:
            self._elements = []

            sql = "SELECT league_id, league_name FROM league where league_id > 0"

            res = db.exec_sql(sql)

            for r in res:
                self._elements.append(
                    League(id=r['league_id'], name=r['league_name']))

    def _get_leagues(self):
        return self.elements

    leagues = property(_get_leagues)
