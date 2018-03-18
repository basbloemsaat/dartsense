#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.event import Event, LeagueRound, LeagueAdjust, Poule, Knockout


def test_event_Event_init():
    event = Event()
    assert isinstance(event, Event)

def test_event_LeagueRound_init():
    event = LeagueRound()
    assert isinstance(event, Event)
    assert isinstance(event, LeagueRound)

def test_event_LeagueAdjust_init():
    event = LeagueAdjust()
    assert isinstance(event, Event)
    assert isinstance(event, LeagueAdjust)

def test_event_Poule_init():
    event = Poule()
    assert isinstance(event, Event)
    assert isinstance(event, Poule)

def test_event_Knockout_init():
    event = Knockout()
    assert isinstance(event, Event)
    assert isinstance(event, Knockout)



    # assert not event.name

#     event = Event(name='test event 1')
#     assert isinstance(event, Event)
#     assert event.name
#     assert event.name == 'test event 1'


# def test_event_load():
#     event = Event(id=pytest.setup_vars['event1_id'])
#     assert isinstance(event, Event)
#     assert event.name == 'test event 1'
