#!/usr/bin/env python3

import pytest
from dartsense.player import Player


def test_player_init():
    player = Player()

    assert isinstance(player, Player)

    assert not player.name

    player = Player(name = 'test player 1')
    assert isinstance(player, Player)
    assert player.name
    assert player.name == 'test player 1'

