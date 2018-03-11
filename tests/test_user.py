#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.user import User


def test_user_init():
    user = User()

    assert isinstance(user, User)
    assert hasattr(user, 'id')
    assert user.id == 0

    assert hasattr(user, 'get_permissions')
    assert callable(user.get_permissions)

    permissions = user.get_permissions()

    assert isinstance(permissions, list)
    assert len(permissions) == 0


