from pprint import pprint
from dartsense import List_C
from dartsense import db


class League:

    def __init__(self, name='', id=0):
        self.id = id
        self.name = name


class LeagueList(List_C):

    def __init__(
        self,
        size=3,
        results=None,
    ):
        List_C.__init__(self, size=size)

    def _search(self, force=False):
        if force or self._elements == None:
            self._elements = []

            sql = "SELECT league_id, league_name FROM league"

            res = db.exec_sql(sql)

            for r in res:
                self._elements.append(League(id=r['league_id'], name=r['league_name']))

    def _get_leagues(self):
        return self.elements

    leagues = property(_get_leagues)
