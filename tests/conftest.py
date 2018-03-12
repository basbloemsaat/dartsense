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
    empty_db()
    cur = db.get_cursor()
    cur.execute("INSERT INTO player (player_name,player_callsigns) VALUES ('test player 1','test player;test player 1')")
    cur.execute("INSERT INTO player (player_name,player_callsigns) VALUES ('test player 2','test player;test player 2')")


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