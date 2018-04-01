#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.event 


def test_event_EventList_init():
    event = dartsense.event.EventList()
    assert isinstance(event, dartsense.event.EventList)

