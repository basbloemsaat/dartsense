from pprint import pprint
from dartsense import List_C
from dartsense import db
from dartsense.player import PlayerList


class Competion:

    def __init__(self, id=0, name='',):
        self.id = id
        self.name = name

        if id and not name:
            sql = "SELECT competition_id, competition_name FROM competition where competition_id=%s LIMIT 1"
            res = db.exec_sql(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['competition_name']

    def _get_players(self):
        player_list = PlayerList(filters={'competition': self.id})
        return player_list

    players = property(_get_players)


class CompetitionList(List_C):

    def __init__(self):
        List_C.__init__(self)

    def _search(self, force=False):
        if force or self._elements == None:
            self._elements = []

            sql = "SELECT competition_id, competition_name FROM competition where competition_id > 0"

            res = db.exec_sql(sql)

            for r in res:
                self._elements.append(
                    Competition(id=r['competition_id'], name=r['competition_name']))

    def _get_competitions(self):
        return self.elements

    competitions = property(_get_competitions)
