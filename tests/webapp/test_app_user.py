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


def test_user_index(client):
    res = client.get('/user')
    assert res.status_code == 302

    res = client.get('/user/')
    assert res.status_code == 302


def test_user_login(client):
    res = client.get('/user/login')
    assert res.status_code == 200

    res = client.get('/user/login/')
    assert res.status_code == 200

# TEMPORARY DISABLED
# def test_user_login_provider(client):
#     res = client.get('/user/login/google')
#     assert res.status_code == 302

# TEMPORARY DISABLED
# def test_user_logout(client):
#     res = client.get('/user/logout')
#     assert res.status_code == 302

#     res = client.get('/user/logout/')
#     assert res.status_code == 302

def test_user_auth(client):
    # no test for now at least
    pass

