#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/"))

import pytest

from pprint import pprint
from dumper import dump

from dartsense import config


def test_config_main():
    assert config.SESSION_SECRET != None
    assert config.SESSION_SECRET != ''

def test_config_database():
    assert config.database != None
    assert isinstance(config.database, dict)
    assert config.database != {}
    assert 'host' in config.database
    assert 'username' in config.database
    assert 'password' in config.database
    assert 'schema' in config.database

def test_config_oauth2():
    assert config.oauth2 != None
    assert isinstance(config.oauth2, dict)
    assert config.oauth2 != {}

    assert 'google' in config.oauth2

