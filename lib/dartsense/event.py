from dartsense import db, List_C


class Event:

    def __init__(self, id=None, type=None):
        pass


class LeagueRound(Event):

    def __init__(self, id=None):
        pass


class LeagueAdjust(Event):

    def __init__(self, id=None):
        pass


class Poule(Event):

    def __init__(self, id=None):
        pass


class Knockout(Event):

    def __init__(self, id=None):
        pass


class EventList(List_C):

    def __init(self):
        self.list = []
