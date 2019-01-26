#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.event
import dartsense.match
import dartsense.player

from pprint import pprint


def test_match_MatchList_init():
    match_list = dartsense.match.MatchList()
    assert isinstance(match_list, dartsense.match.MatchList)

    # matchlists without filters are empty
    assert len(match_list) == 0


def test_match_list_filter_competition(setup_db):
    match_list = dartsense.match.MatchList(
        filters={'event': pytest.setup_vars['testcompetition1_round1_id']}
    )

    assert len(match_list) == 2
