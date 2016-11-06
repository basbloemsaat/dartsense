#!/usr/bin/env python3

import pytest
from dartsense.competition import Competition


def test_competition_init():
    competition = Competition()

    assert competition
    assert isinstance(competition, Competition)
