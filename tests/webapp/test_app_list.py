#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../lib/"))

import pytest

from dartsense.webapp import app as tl_app
tl_app.config['DEBUG'] = True 
tl_app.config['TESTING'] = True

@pytest.fixture
def app():
    return tl_app

def test_list_index(client):
    res = client.get('/list')
    assert res.status_code == 200

    res = client.get('/list/')
    assert res.status_code == 200

def test_list_competitions(client):
    res = client.get('/list/competitions')
    assert res.status_code == 200

    res = client.get('/list/competitions/')
    assert res.status_code == 200

def test_list_competition(client):
    res = client.get('/list/competition/123')
    assert res.status_code == 200

def test_list_player(client):
    res = client.get('/list/player/456')
    assert res.status_code == 200

