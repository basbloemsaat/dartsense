#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.player import Player
import dartsense.competition


def test_player_init(setup_db):
    player = Player()
    assert isinstance(player, Player)

    assert not player.name

    player = Player(name='test player 1')
    assert isinstance(player, Player)
    assert player.name
    assert player.name == 'test player 1'


def test_player_load(setup_db):
    player = Player(id=pytest.setup_vars['player1_id'])
    assert isinstance(player, Player)
    assert player.name == 'test player 1'

def test_player_Competitions(setup_db):
    player = Player(id=pytest.setup_vars['player1_id'])
    assert hasattr(player, 'competitions')
    competitions = player.competitions

    assert isinstance(competitions, dartsense.competition.CompetitionList)
    assert len(competitions) == 1
    assert isinstance(competitions[0],  dartsense.competition.Competition)
    assert competitions[0].name == 'test league 1'


