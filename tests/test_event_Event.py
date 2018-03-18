#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.event import Event


def test_event_init():
    event = Event()
    assert isinstance(event, Event)

    # assert not event.name

#     event = Event(name='test event 1')
#     assert isinstance(event, Event)
#     assert event.name
#     assert event.name == 'test event 1'


# def test_event_load():
#     event = Event(id=pytest.setup_vars['event1_id'])
#     assert isinstance(event, Event)
#     assert event.name == 'test event 1'
