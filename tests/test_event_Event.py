#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.competition
import dartsense.event


def test_event_Event_init(setup_db):
    event = dartsense.event.Event()
    assert isinstance(event, dartsense.event.Event)

    assert hasattr(event, 'id')
    assert event.id == None

    assert hasattr(event, 'type')
    assert event.type == None

    assert hasattr(event, 'name')
    assert event.name == None

    assert hasattr(event, 'competition')
    assert event.competition == None


def test_event_LeagueRound_init(setup_db):
    event = dartsense.event.LeagueRound()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueRound)

    assert hasattr(event, 'type')
    assert event.type == 'league_round'
    assert event.name == None

    event = dartsense.event.Event(
        id=pytest.setup_vars['testcompetition1_round1_id'])
    assert event.id != None
    assert event.id == pytest.setup_vars['testcompetition1_round1_id']
    assert event.name == 'test competition 1 round 1'
    assert event.type == 'league_round'
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueRound)

    assert isinstance(event.competition, dartsense.competition.Competition)
    assert event.competition.id == pytest.setup_vars['testleague1_id']


def test_event_LeagueRound_update(setup_db):
    event = dartsense.event.Event(
        id=pytest.setup_vars['testcompetition1_round1_id'])

    assert isinstance(event.competition, dartsense.competition.Competition)
    assert event.competition.id == pytest.setup_vars['testleague1_id']

    event.competition = pytest.setup_vars['testleague2_id']
    assert event.competition.id == pytest.setup_vars['testleague2_id']

    assert hasattr(event, 'save')
    event.save()

    event = None
    event = dartsense.event.Event(
        id=pytest.setup_vars['testcompetition1_round1_id'])

    assert event.competition.id == pytest.setup_vars['testleague2_id']
    event.competition = dartsense.competition.Competition(
        id=pytest.setup_vars['testleague1_id'])
    assert event.competition.id == pytest.setup_vars['testleague1_id']
    event.save()

    event = None
    event = dartsense.event.Event(
        id=pytest.setup_vars['testcompetition1_round1_id'])

    assert event.competition.id == pytest.setup_vars['testleague1_id']


def test_event_LeagueRound_save_new(setup_db):
    event = dartsense.event.LeagueRound(
        name='testround', competition=pytest.setup_vars['testleague2_id'])

    assert event.id == None
    assert event.name == 'testround'
    new_id = event.save()

    assert isinstance(new_id, int)
    assert new_id > 0
    assert event.id == new_id

    event = None
    event = dartsense.event.Event(id=new_id)
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueRound)
    assert event.id == new_id
    assert event.name == 'testround'


def test_event_LeagueAdjust_init(setup_db):
    event = dartsense.event.LeagueAdjust()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueAdjust)

    assert hasattr(event, 'type')
    assert event.type == 'league_adjust'
    assert event.name == None

    event = dartsense.event.Event(
        id=pytest.setup_vars['testcompetition2_adjustment_id'])
    assert event.id != None
    assert event.id == pytest.setup_vars['testcompetition2_adjustment_id']
    assert event.name == 'test competition 2 adjustment'
    assert event.type == 'league_adjust'
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueAdjust)

    assert isinstance(event.competition, dartsense.competition.Competition)
    assert event.competition.id == pytest.setup_vars['testleague2_id']


def test_event_Poule_init(setup_db):
    event = dartsense.event.Poule()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Poule)

    assert hasattr(event, 'type')
    assert event.type == 'poule'
    assert event.name == None

    event = dartsense.event.Event(id=pytest.setup_vars['testpoule1_id'])
    assert event.id != None
    assert event.id == pytest.setup_vars['testpoule1_id']
    assert event.name == 'test poule 1'
    assert event.type == 'poule'
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Poule)

    assert isinstance(event.competition, dartsense.competition.Competition)
    assert event.competition.id == pytest.setup_vars['testtournament1_id']


def test_event_Knockout_init(setup_db):
    event = dartsense.event.Knockout()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Knockout)

    assert hasattr(event, 'type')
    assert event.type == 'knockout'
    assert event.name == None

    event = dartsense.event.Event(id=pytest.setup_vars['testknockout1_id'])
    assert event.id != None
    assert event.id == pytest.setup_vars['testknockout1_id']
    assert event.name == 'test knockout 1'
    assert event.type == 'knockout'
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Knockout)

    assert isinstance(event.competition, dartsense.competition.Competition)
    assert event.competition.id == pytest.setup_vars['testtournament1_id']

#
