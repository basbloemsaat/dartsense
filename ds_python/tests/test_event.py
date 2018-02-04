#!/usr/bin/env python3

import os
import pytest
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.event import Event


def test_event_init():
    event = Event()
    assert isinstance(event, Event)


