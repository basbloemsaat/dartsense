#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.match 
import dartsense.player 


def test_match_Match_init():
    match = dartsense.match.Match()
    assert isinstance(match, dartsense.match.Match)

    assert hasattr(match, 'id')
    assert match.id == None

    assert hasattr(match, 'player_1')
    assert match.player_1 == None

    assert hasattr(match, 'player_1')
    assert match.player_2 == None

def test_match_Match_load(setup_db):
    match = dartsense.match.Match(id=pytest.setup_vars['match1_id'])
    assert isinstance(match, dartsense.match.Match)
    
    assert hasattr(match, 'id')
    assert match.id == pytest.setup_vars['match1_id']

    assert hasattr(match, 'player_1')
    assert isinstance(match.player_1, dartsense.player.Player)
    assert match.player_1.id == pytest.setup_vars['player1_id']

    assert hasattr(match, 'player_2')
    assert isinstance(match.player_2, dartsense.player.Player)
    assert match.player_2.id == pytest.setup_vars['player2_id']






