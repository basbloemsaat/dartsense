#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.competition
import dartsense.event
import dartsense.player


def test_competition_init():
    competition = dartsense.competition.Competition()

    assert isinstance(competition, dartsense.competition.Competition)
    assert not competition.name

    competition = dartsense.competition.Competition(name='test league 1')
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'name')
    assert competition.name == 'test league 1'


def test_competition_by_id(setup_db):
    competition = dartsense.competition.Competition(
        id=pytest.setup_vars['testleague1_id'])
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'id')
    assert competition.id == pytest.setup_vars['testleague1_id']
    assert hasattr(competition, 'name')
    assert competition.name == 'test league 1'


def test_create_and_delete_new_competition():
    competition = dartsense.competition.Competition(
        name='test new competition')
    assert isinstance(competition, dartsense.competition.Competition)
    assert hasattr(competition, 'name')
    assert competition.name == 'test new competition'

    assert hasattr(competition, 'id')
    assert competition.id == 0

    new_id = competition.save()
    assert new_id > 0
    assert competition.id == new_id

    competition2 = dartsense.competition.Competition(id=new_id)
    assert isinstance(competition2, dartsense.competition.Competition)
    assert competition2.id == new_id
    assert competition2.name == 'test new competition'

    competition2 = None

    competition.delete()
    assert competition.id == 0
    assert competition.name == ''

    competition2 = dartsense.competition.Competition(id=new_id)
    assert isinstance(competition2, dartsense.competition.Competition)
    assert competition2.id == -1
    assert competition2.name == ''


def test_competition_players(setup_db):
    competition = dartsense.competition.Competition(
        id=pytest.setup_vars['testleague1_id'])
    assert hasattr(competition, 'players')

    assert isinstance(competition.players, dartsense.player.PlayerList)
    assert len(competition.players) == 4


def test_competition_events(setup_db):
    competition = dartsense.competition.Competition(
        id=pytest.setup_vars['testleague1_id'])

    assert hasattr(competition, 'events')
    assert isinstance(competition.events, dartsense.event.EventList)
    # assert len(competition.events) == 2
