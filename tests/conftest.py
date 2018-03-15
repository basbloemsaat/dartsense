import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../etc/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/"))
os.environ["DARTSENSE_ENV"] = "TEST"
os.environ["DARTSENSE_SCHEMA"] = "dartsense_test"

import pytest
from dartsense import db


@pytest.fixture(scope="session")
def setup_db():
    # setup a basic state to run tests

    pytest_setup_vars = {}

    empty_db()
    cur = db.get_cursor()
    cur.execute("INSERT INTO player (player_name,player_callsigns) VALUES ('test player 1','test player;test player 1')")
    pytest_setup_vars['player1_id'] = cur.lastrowid
    cur.execute("INSERT INTO player (player_name,player_callsigns) VALUES ('test player 2','test player;test player 2')")
    pytest_setup_vars['player2_id'] = cur.lastrowid

    cur.execute("INSERT INTO user (user_name, user_email) VALUES ('test user', 'test@test.com')")
    pytest_setup_vars['testuser_id'] = cur.lastrowid

    cur.execute("INSERT INTO usercredential (user_id, usercred_provider, usercred_value) VALUES (%s, 'google','test@test.org')", [pytest_setup_vars['testuser_id']])

    pytest.setup_vars = pytest_setup_vars


def empty_db():
    # clear the database for tests
    cur = db.get_cursor()

    cur.execute("DELETE FROM `group_league`")
    cur.execute("DELETE FROM `group_permission`")
    cur.execute("DELETE FROM `user_group`")
    cur.execute("DELETE FROM `finish`")
    cur.execute("DELETE FROM `match`")
    cur.execute("DELETE FROM `event` WHERE event_id>0")
    cur.execute("DELETE FROM `group` WHERE group_id>0")
    cur.execute("DELETE FROM `player_alias`")
    cur.execute("DELETE FROM `player`")
    cur.execute("DELETE FROM `usercredential`")
    cur.execute("DELETE FROM `user`")
    cur.execute("DELETE FROM `league` WHERE league_id>0")