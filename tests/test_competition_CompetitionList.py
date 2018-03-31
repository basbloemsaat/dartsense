#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.competition 


def test_competitionlist_init():
    competition_list = dartsense.competition.CompetitionList()

    assert isinstance(competition_list, dartsense.competition.CompetitionList)
    assert len(competition_list) == 4


def test_competitionlist_filter():
    competition_list = dartsense.competition.CompetitionList(filters={'player':pytest.setup_vars['player1_id']})

    assert isinstance(competition_list, dartsense.competition.CompetitionList)
    assert len(competition_list) == 1

    