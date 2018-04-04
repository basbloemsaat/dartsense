#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.competition
from dartsense.player import PlayerList


def test_competition_init():
    competition = dartsense.competition.Competition()

    assert isinstance(competition, dartsense.competition.Competition)
    assert not competition.name

    competition = dartsense.competition.Competition(name='test league 1')
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'name')
    assert competition.name == 'test league 1'


def test_competition_by_id(setup_db):
    competition = dartsense.competition.Competition(id=pytest.setup_vars['testleague1_id'])
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'id')
    assert competition.id == pytest.setup_vars['testleague1_id']
    assert hasattr(competition, 'name')
    assert competition.name == 'test league 1'


def test_competition_players():
    competition = dartsense.competition.Competition(id=pytest.setup_vars['testleague1_id'])
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'players')

    assert isinstance(competition.players, PlayerList)
    assert len(competition.players) == 4
