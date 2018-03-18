#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.player import Player


def test_player_init():
    player = Player()
    assert isinstance(player, Player)

    assert not player.name

    player = Player(name='test player 1')
    assert isinstance(player, Player)
    assert player.name
    assert player.name == 'test player 1'


def test_player_load():
    player = Player(id=pytest.setup_vars['player1_id'])
    assert isinstance(player, Player)
    assert player.name == 'test player 1'
