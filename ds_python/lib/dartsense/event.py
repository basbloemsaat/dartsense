class Event:
    def __init__(self, date=None):
        pass


class Match(Event):

    def __init__(self, id=0, player1=None, player2=None, date=None, round=None,board=None, sets=1):
        self.player1 = player1
        self.player2 = player2
        self.date = date
        self.round = round
        self.board = board


class Tournament(Event):

    def __init__(self, player=None, date=None, matches=0, points=0):
        self.player = player
        self.date = date
        self.matches = matches
        self.points = points


class EventList():
    def __init(self):
        self.list=[]

    

