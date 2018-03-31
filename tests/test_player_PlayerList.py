#!/usr/bin/env python3

import os
import pytest
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.player


player_list = None


def test_player_list_init(setup_db):
    player_list = dartsense.player.PlayerList()

    assert isinstance(player_list, dartsense.player.PlayerList)
    assert len(player_list) == 4

    for player in player_list:
        assert isinstance(player, dartsense.player.Player)


def test_player_list_filter(setup_db):
    player_list = dartsense.player.PlayerList(
        filters={'competition': pytest.setup_vars['testleague1_id']}
    )
    assert len(player_list) == 2


def test_player_list_search(setup_db):
    player_list = dartsense.player.PlayerList(
        search='player 3'
    )
    assert len(player_list) == 1

    player_list = dartsense.player.PlayerList(
        filters={'competition': pytest.setup_vars['testleague2_id']},
        search='player 3'
    )
    assert len(player_list) == 1
