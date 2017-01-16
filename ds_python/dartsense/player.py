from pprint import pprint
import hashlib


class Player:

    def __init__(self, name='', id=0):
        self.id = id
        self.name = name
        self.aliases = []

        if self.id == 0:
            self.id = hashlib.sha256(self.name.encode()).hexdigest()


class PlayerList:

    def __init__(self):
        self.list = {}

    def __len__(self):
        return 0+len(self.list)

    def add_player(self, player):
        self.list[player.id] = player
