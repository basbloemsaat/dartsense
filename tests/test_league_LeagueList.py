#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.league import LeagueList


def test_league_init():
    league_list = LeagueList()

    assert isinstance(league_list, LeagueList)
    assert len(league_list) == 3
   