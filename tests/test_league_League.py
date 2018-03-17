#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.league import League


def test_league_init():
    league = League()

    assert isinstance(league, League)
    assert not league.name

    league = League(name='test league 1')
    assert isinstance(league, League)
    assert hasattr(league, 'name')
    assert league.name == 'test league 1'
