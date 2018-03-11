#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense.user import User


def test_user_init():
    user = User()

    assert isinstance(user, User)

