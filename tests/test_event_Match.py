#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.event
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

    assert hasattr(match, 'event')
    assert match.event == None

    assert hasattr(match, 'player_1_score')
    assert match.player_1_score == 0
    assert hasattr(match, 'player_2_score')
    assert match.player_2_score == 0

    assert hasattr(match, 'player_1_180s')
    assert match.player_1_180s == 0
    assert hasattr(match, 'player_2_180s')
    assert match.player_2_180s == 0

    assert hasattr(match, 'player_1_lollies')
    assert match.player_1_lollies == 0
    assert hasattr(match, 'player_2_lollies')
    assert match.player_2_lollies == 0

    assert hasattr(match, 'player_1_finishes')
    assert match.player_1_finishes == []
    assert hasattr(match, 'player_2_finishes')
    assert match.player_2_finishes == []


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

    assert isinstance(match.event, dartsense.event.Event)
    assert match.event.id == pytest.setup_vars['testcompetition1_round1_id']


def test_match_Match_save(setup_db):
    match = dartsense.match.Match()
    assert match.id == None

    assert hasattr(match, 'save')
    assert match.save() == False
    assert match.id == None



