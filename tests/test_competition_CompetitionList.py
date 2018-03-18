#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.competition import CompetitionList


def test_competitionlist_init():
    competition_list = CompetitionList()

    assert isinstance(competition_list, CompetitionList)
    assert len(competition_list) == 4


   
