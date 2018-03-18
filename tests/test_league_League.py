#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.league import League
from dartsense.player import PlayerList


def test_league_init():
    league = League()

    assert isinstance(league, League)
    assert not league.name

    league = League(name='test league 1')
    assert isinstance(league, League)
    assert hasattr(league, 'name')
    assert league.name == 'test league 1'

def test_league_by_id(setup_db):
    league = League(id=pytest.setup_vars['testleague1_id'])
    assert isinstance(league, League)
    assert hasattr(league, 'id')
    assert league.id == pytest.setup_vars['testleague1_id']
    assert hasattr(league, 'name')
    assert league.name == 'test league 1'

def test_league_players():
    league = League(id=pytest.setup_vars['testleague1_id'])
    assert isinstance(league, League)
    assert hasattr(league, 'players')

    assert isinstance(league.players, PlayerList)
    assert len(league.players) == 2
