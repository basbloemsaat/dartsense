#!/usr/bin/env python3

import pytest
import os
import sys
from pprint import pprint


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

from dartsense import db


def test_db_select():
    rows = db.exec_select('show tables')
    assert isinstance(rows, list)
    assert len(rows) > 0
    assert isinstance(rows[0], dict)
    assert 'Tables_in_dartsense_test' in rows[0]

    db.connection = True
    rows = db.exec_select('show tables')

    assert isinstance(rows, list)
    assert len(rows) > 0


def test_db_insert(setup_db):
    new_id_1 = db.exec_insert(
        """
        INSERT INTO user (user_name, user_email)
        VALUES ('test 1', 'test1@test.com')
        """
    )

    assert isinstance(new_id_1, int)
    assert new_id_1 > 0

    new_id_2 = db.exec_insert(
        """
        INSERT INTO user (user_name, user_email)
        VALUES (%s,%s)
        """
        , ['test 1', 'test1@test.com']
    )

    assert isinstance(new_id_2, int)
    assert new_id_2 > 0
