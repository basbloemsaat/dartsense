class Match:

    def __init__(self, id=0, player1=None, player2=None, date=None, round=None, sets=1):
        self.player1 = player1
        self.player2 = player2
        self.date = date
        self.round = round


class Set:

    def __init__(self, number, legs=1):
        self.number = number


class Leg:

    def __init__(self, number):
        self.number = number
