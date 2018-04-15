#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.event


def test_event_EventList_init():
    event_list = dartsense.event.EventList()
    assert isinstance(event_list, dartsense.event.EventList)

    assert len(event_list) == 9

    for event in event_list:
        assert isinstance(event, dartsense.event.Event)


def test_event_list_filter_competition(setup_db):
    event_list = dartsense.event.EventList(
        filters={'competition': pytest.setup_vars['testleague1_id']}
    )

    assert len(event_list) == 2

def test_event_list_filter_player(setup_db):
    event_list = dartsense.event.EventList(
        filters={'player': pytest.setup_vars['player1_id']}
    )

    assert len(event_list) == 1
    

