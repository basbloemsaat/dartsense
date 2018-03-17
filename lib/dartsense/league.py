from pprint import pprint


class League:

    def __init__(self, name='', id=0):
        self.id = id
        self.name = name


class LeagueList:

    def __init__(self):
        self.list = {}

    def __len__(self):
        return 0+len(self.list)

    def add_league(self, league):
        self.list[league.id] = league
        return league

    def find(self, search):
        leagues = [self.list[p] for p in self.list if self.list[p].name == search]
        return leagues


