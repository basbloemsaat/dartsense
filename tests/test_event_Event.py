#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

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

    event = dartsense.event.Event(id=pytest.setup_vars['testcompetition1_round1_id'])
    assert event.id != None
    assert event.id == pytest.setup_vars['testcompetition1_round1_id']
    assert event.name == 'test competition 1 round 1'
    # assert event.type != None


def test_event_LeagueRound_init(setup_db):
    event = dartsense.event.LeagueRound()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueRound)

    assert hasattr(event, 'type')
    assert event.type == 'league_round'


def test_event_LeagueAdjust_init(setup_db):
    event = dartsense.event.LeagueAdjust()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.LeagueAdjust)

    assert hasattr(event, 'type')
    assert event.type == 'league_adjust'


def test_event_Poule_init(setup_db):
    event = dartsense.event.Poule()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Poule)

    assert hasattr(event, 'type')
    assert event.type == 'poule'


def test_event_Knockout_init(setup_db):
    event = dartsense.event.Knockout()
    assert isinstance(event, dartsense.event.Event)
    assert isinstance(event, dartsense.event.Knockout)

    assert hasattr(event, 'type')
    assert event.type == 'knockout'

    # assert not event.name

#     event = Event(name='test event 1')
#     assert isinstance(event, Event)
#     assert event.name
#     assert event.name == 'test event 1'


# def test_event_load():
#     event = Event(id=pytest.setup_vars['event1_id'])
#     assert isinstance(event, Event)
#     assert event.name == 'test event 1'
