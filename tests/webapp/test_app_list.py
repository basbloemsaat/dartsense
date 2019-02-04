#!/usr/bin/env python3

import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../lib/"))

import re

from dartsense.webapp import app as tl_app
tl_app.config['DEBUG'] = True
tl_app.config['TESTING'] = True


@pytest.fixture
def app(setup_db):
    return tl_app


def test_list_index(client):
    tl_app.config['TEST_LOGIN'] = False
    res = client.get('/list')
    assert res.status_code == 401

    res = client.get('/list/')
    assert res.status_code == 401

    tl_app.config['TEST_LOGIN'] = True
    res = client.get('/user', follow_redirects=True)

    cookie = res.headers['Set-Cookie']
    match = re.search(r'dartsense_session=([^;]+);',cookie)
    sessionid = match.group(1)

    client.set_cookie('localhost', 'dartsense_session',sessionid)
    res = client.get('/list/')
    assert res.status_code == 200
    


# def test_list_competitions(client):
#     res = client.get('/list/competitions')
#     assert res.status_code == 200

#     res = client.get('/list/competitions/')
#     assert res.status_code == 200


# def test_list_competition(client):
#     res = client.get('/list/competition/' +
#                      str(pytest.setup_vars['testtournament1_id']))
#     assert res.status_code == 200
#     res = client.get('/list/competition/99999999')
#     assert res.status_code == 404


# def test_list_player(client):
#     res = client.get('/list/player/' + str(pytest.setup_vars['player1_id']))
#     assert res.status_code == 200
#     res = client.get('/list/player/999999999')
#     assert res.status_code == 404


# def test_list_organisations(client):
#     res = client.get('/list/organisations')
#     assert res.status_code == 200

# def test_list_organisation(client):
#     res = client.get('/list/organisation/' + str(pytest.setup_vars['organisation1_id']))

# def test_list_event(client):
#     res = client.get('/list/event/' + str(pytest.setup_vars['testcompetition1_round1_id']))
#     assert res.status_code == 200

