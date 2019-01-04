#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.competition
import dartsense.player


def test_player_init(setup_db):
    player = dartsense.player.Player()
    assert isinstance(player, dartsense.player.Player)

    assert not player.name

    player = dartsense.player.Player(name='test player 1')
    assert isinstance(player, dartsense.player.Player)
    assert player.name
    assert player.name == 'test player 1'


def test_create_new_player(setup_db):
    player = dartsense.player.Player(name='test player create')
    assert isinstance(player, dartsense.player.Player)
    assert player.id == 0

    player.save()
    assert player.id > 0

    new_id = player.id

    player2 = dartsense.player.Player(id=new_id)
    assert isinstance(player2, dartsense.player.Player)

    assert player2.id == new_id
    player2 = None

    player.delete()
    player2 = dartsense.player.Player(id=new_id)
    assert isinstance(player2, dartsense.player.Player)
    assert player2.id == 0


def test_player_load(setup_db):
    player = dartsense.player.Player(id=pytest.setup_vars['player1_id'])
    assert isinstance(player, dartsense.player.Player)
    assert player.name == 'test player 1'


def test_player_Competitions(setup_db):
    player = dartsense.player.Player(id=pytest.setup_vars['player1_id'])
    assert hasattr(player, 'competitions')
    competitions_list = player.competitions

    assert isinstance(competitions_list, dartsense.competition.CompetitionList)
    assert len(competitions_list) == 1
    assert isinstance(competitions_list[0],  dartsense.competition.Competition)
    assert competitions_list[0].name == 'test league 1'
