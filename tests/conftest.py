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

    # players
    sql = "INSERT INTO player (player_name,player_callsigns) VALUES (%s,%s)"
    cur.execute(sql, ['test player 1', 'test player;test player 1'])
    pytest_setup_vars['player1_id'] = cur.lastrowid
    cur.execute(sql, ['test player 2', 'test player;test player 2'])
    pytest_setup_vars['player2_id'] = cur.lastrowid
    cur.execute(sql, ['test player 3', 'test player;test player 3'])
    pytest_setup_vars['player3_id'] = cur.lastrowid
    cur.execute(sql, ['test player 4', 'test player;test player 4'])
    pytest_setup_vars['player4_id'] = cur.lastrowid

    # users
    sql = "INSERT INTO user (user_name, user_email) VALUES (%s, %s)"
    cur.execute(sql, ['test user', 'test@test.com'])
    pytest_setup_vars['testuser_id'] = cur.lastrowid

    # usercredentials
    sql = "INSERT INTO usercredential (user_id, usercred_provider, usercred_value) VALUES (%s,%s,%s)"
    cur.execute(sql, [pytest_setup_vars['testuser_id'],
                      'google', 'test@test.org', ])

    # competition
    sql = "INSERT INTO competition (competition_name) VALUES (%s)"
    cur.execute(sql, ['test competition 1'])
    pytest_setup_vars['testcompetition1_id'] = cur.lastrowid
    cur.execute(sql, ['test competition 2'])
    pytest_setup_vars['testcompetition2_id'] = cur.lastrowid

    # competition players
    sql = "INSERT INTO competition_player (competition_id, player_id) VALUES (%s,%s)"
    cur.execute(sql, [pytest_setup_vars['testcompetition1_id'],
                      pytest_setup_vars['player1_id']])
    cur.execute(sql, [pytest_setup_vars['testcompetition1_id'],
                      pytest_setup_vars['player2_id']])
    cur.execute(sql, [pytest_setup_vars['testcompetition2_id'],
                      pytest_setup_vars['player3_id']])
    cur.execute(sql, [pytest_setup_vars['testcompetition2_id'],
                      pytest_setup_vars['player4_id']])

    # events
    sql = "INSERT INTO event (competition_id, event_type, event_name) VALUES (%s,%s,%s)"
    cur.execute(sql, [pytest_setup_vars['testcompetition1_id'],
                      'league_round', 'test competition 1 round 1'])
    pytest_setup_vars['testcompetition1_round1_id'] = cur.lastrowid
    cur.execute(sql, [pytest_setup_vars['testcompetition1_id'],
                      'league_round', 'test competition 1 round 2'])
    pytest_setup_vars['testcompetition1_round2_id'] = cur.lastrowid
    cur.execute(sql, [pytest_setup_vars['testcompetition2_id'],
                      'league_round', 'test competition 2 round 1'])
    pytest_setup_vars['testcompetition2_round1_id'] = cur.lastrowid
    cur.execute(sql, [pytest_setup_vars['testcompetition2_id'],
                      'league_round', 'test competition 2 round 2'])
    pytest_setup_vars['testcompetition2_round2_id'] = cur.lastrowid
    cur.execute(sql, [pytest_setup_vars['testcompetition2_id'],
                      'league_round', 'test competition 2 round 3'])
    pytest_setup_vars['testcompetition2_round3_id'] = cur.lastrowid
    cur.execute(sql, [0, 'poule', 'test poule 1'])
    pytest_setup_vars['testpoule1_id'] = cur.lastrowid
    cur.execute(sql, [0, 'poule', 'test poule 2'])
    pytest_setup_vars['testpoule2_id'] = cur.lastrowid

    pytest.setup_vars = pytest_setup_vars


def empty_db():
    # clear the database for tests
    cur = db.get_cursor()

    cur.execute("DELETE FROM `group_competition`")
    cur.execute("DELETE FROM `group_permission`")
    cur.execute("DELETE FROM `user_group`")
    cur.execute("DELETE FROM `finish`")
    cur.execute("DELETE FROM `match`")
    cur.execute("DELETE FROM `event` WHERE event_id>0")
    cur.execute("DELETE FROM `group` WHERE group_id>0")
    cur.execute("DELETE FROM `player_alias`")
    cur.execute("DELETE FROM `competition_player`")
    cur.execute("DELETE FROM `player`")
    cur.execute("DELETE FROM `usercredential`")
    cur.execute("DELETE FROM `user`")
    cur.execute("DELETE FROM `competition` WHERE competition_id>0")
