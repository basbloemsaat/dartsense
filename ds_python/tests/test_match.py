#!/usr/bin/env python3

import pytest
from dartsense.match import Match
from dartsense.match import Set
from dartsense.match import Leg


def test_match_init():
    match = Match()

    assert match
    assert isinstance(match, Match)
