class Team:

    def __init__(self, name='', id=0, players=[]):
        self.id = name
        self.name = name
        self.players = players

    def add_player(self, player):
        self.players.append(player)
