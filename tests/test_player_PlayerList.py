#!/usr/bin/env python3

import os
import pytest
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

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

    player = Player(name='test player 1')
    player_list.add_player(player)
    assert len(player_list) == 1

    player_list.add_player(Player(name='test player 2'))
    assert len(player_list) == 2


def test_player_list_find_player():
    player_list = PlayerList()
    player_list.add_player(Player(name='test player 1'))
    player_list.add_player(Player(name='test player 2'))
    player_list.add_player(Player(name='test player 3'))

    players = player_list.find('test player 2')

    assert len(players) == 1
    assert isinstance(players[0], Player)
    assert players[0].name == 'test player 2'


@pytest.fixture
def basic_list():
    player_list = PlayerList()
