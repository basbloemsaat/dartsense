#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/"))

import pytest

from pprint import pprint
from dumper import dump


from dartsense import config


def test_test_index():
    assert config.SESSION_SECRET != None
    assert config.SESSION_SECRET != ''

