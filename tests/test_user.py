#!/usr/bin/env python3

import pytest
import os
import sys

from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.user import User


def test_user_init():
    user = User()

    assert isinstance(user, User)
    assert hasattr(user, 'id')
    assert user.id == None

    assert hasattr(user, 'get_permissions')
    assert callable(user.get_permissions)

    permissions = user.get_permissions()

    assert isinstance(permissions, list)
    assert len(permissions) == 0


def test_user_db(setup_db):
    # pprint(pytest.setup_vars)
    user = User(id=pytest.setup_vars['testuser_id'])
    assert isinstance(user, User)
    assert hasattr(user, 'name')
    assert user.name == 'test user'

    assert hasattr(user, 'email')
    assert user.email == 'test@test.com'


def test_user_login(setup_db):
    user = User()
    assert hasattr(user, 'login')
    assert callable(user.login)

    assert user.id == None
    assert user.login('google', 'test@test.org')
    assert user.id == pytest.setup_vars['testuser_id']

    assert hasattr(user, 'name')
    assert user.name == 'test user'
