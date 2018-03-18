#!/usr/bin/env python3

import os
import pytest
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.player import Player
from dartsense.player import PlayerList


player_list = None


def test_player_list_init(setup_db):
    player_list = PlayerList()

    assert isinstance(player_list, PlayerList)
    assert len(player_list) == 4

    for player in player_list:
        assert isinstance(player, Player)

def test_player_list_filter(setup_db):
    player_list = PlayerList(filters={'league':pytest.setup_vars['testleague1_id']})
    assert len(player_list) == 2

