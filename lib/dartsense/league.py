from pprint import pprint
from dartsense import List_C


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

    # def add_league(self, league):
    #     self.list[league.id] = league
    #     return league

    # def find(self, search):
    #     leagues = [self.list[p]
    #                for p in self.list if self.list[p].name == search]
    #     return leagues

    def _get_leagues(self):
        return self.elements

    leagues = property(_get_leagues)
