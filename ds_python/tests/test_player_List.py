#!/usr/bin/env python3

import pytest
from pprint import pprint

from dartsense.player import Player
from dartsense.player import PlayerList


def test_player_list_init():
    player_list = PlayerList()

    assert player_list
    assert isinstance(player_list, PlayerList)

    a = len(player_list)
    pprint(a)
