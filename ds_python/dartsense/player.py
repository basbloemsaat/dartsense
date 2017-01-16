from pprint import pprint


class Player:

    def __init__(self, name='', id=0):
        self.id = id
        self.name = name


class PlayerList:

    def __init__(self):
        self.list = {}

    def __len__(self):
        return 0+len(self.list)
