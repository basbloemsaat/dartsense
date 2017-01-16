#!/usr/bin/env python3

import pytest
from pprint import pprint

from dartsense.player import Player
from dartsense.player import PlayerList


player_list = None

def test_player_list_init():
    player_list = PlayerList()

    assert isinstance(player_list, PlayerList)
    assert len(player_list) == 0



def test_player_list_add_player():
    player_list = PlayerList()
    assert len(player_list) == 0

    player = Player(name = 'test player 1')
    player_list.add_player(player)
    assert len(player_list) == 1

    player_list.add_player(Player(name = 'test player 2'))
    assert len(player_list) == 2

    pprint(player_list.list)


@pytest.fixture
def basic_list():
    player_list = PlayerList()