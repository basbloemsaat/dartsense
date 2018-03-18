#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.competition import Competition
from dartsense.player import PlayerList


def test_competition_init():
    competition = Competition()

    assert isinstance(competition, Competition)
    assert not competition.name

    competition = Competition(name='test competition 1')
    assert isinstance(competition, Competition)
    assert hasattr(competition, 'name')
    assert competition.name == 'test competition 1'

def test_competition_by_id(setup_db):
    competition = Competition(id=pytest.setup_vars['testcompetition1_id'])
    assert isinstance(competition, Competition)
    assert hasattr(competition, 'id')
    assert competition.id == pytest.setup_vars['testcompetition1_id']
    assert hasattr(competition, 'name')
    assert competition.name == 'test competition 1'

def test_competition_players():
    competition = Competition(id=pytest.setup_vars['testcompetition1_id'])
    assert isinstance(competition, Competition)
    assert hasattr(competition, 'players')

    assert isinstance(competition.players, PlayerList)
    assert len(competition.players) == 2
