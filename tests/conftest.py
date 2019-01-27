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

    # players
    sql = "INSERT INTO player (player_name,player_callsigns) VALUES (%s,%s)"
    cur = db.exec_sql(sql, ['test player 1', 'test player;test player 1'])
    pytest_setup_vars['player1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test player 2', 'test player;test player 2'])
    pytest_setup_vars['player2_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test player 3', 'test player;test player 3'])
    pytest_setup_vars['player3_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test player 4', 'test player;test player 4'])
    pytest_setup_vars['player4_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test player 5', 'test player;test player 5'])
    pytest_setup_vars['player5_id'] = cur.lastrowid

    # users
    sql = "INSERT INTO user (user_name, user_email) VALUES (%s, %s)"
    cur = db.exec_sql(sql, ['test user', 'test@test.com'])
    pytest_setup_vars['testuser_id'] = cur.lastrowid

    # organisations
    sql = "INSERT INTO organisation (organisation_name) VALUES (%s)"
    cur = db.exec_sql(sql, ['Test Organisation 1'])
    pytest_setup_vars['organisation1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['Test Organisation 2'])
    pytest_setup_vars['organisation2_id'] = cur.lastrowid

    # usercredentials
    sql = "INSERT INTO usercredential (user_id, usercred_provider, usercred_value) VALUES (%s,%s,%s)"
    cur = db.exec_sql(sql, [pytest_setup_vars['testuser_id'],
                            'google', 'test@test.org', ])

    # competition
    sql = "INSERT INTO competition (competition_name, competition_type, organisation_id) VALUES (%s,%s,%s)"
    cur = db.exec_sql(sql, ['test league 1', 'league',
                            pytest_setup_vars['organisation1_id']])
    pytest_setup_vars['testleague1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test league 2', 'league',
                            pytest_setup_vars['organisation2_id']])
    pytest_setup_vars['testleague2_id'] = cur.lastrowid

    cur = db.exec_sql(sql, ['test tournament 1', 'tournament',
                            pytest_setup_vars['organisation1_id']])
    pytest_setup_vars['testtournament1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, ['test tournament 2', 'tournament',
                            pytest_setup_vars['organisation2_id']])
    pytest_setup_vars['testtournament2_id'] = cur.lastrowid

    # competition players
    sql = "INSERT INTO competition_player (competition_id, player_id) VALUES (%s,%s)"
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            pytest_setup_vars['player1_id']])
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            pytest_setup_vars['player2_id']])
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            pytest_setup_vars['player3_id']])
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            pytest_setup_vars['player4_id']])

    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            pytest_setup_vars['player3_id']])
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            pytest_setup_vars['player4_id']])

    # events
    sql = "INSERT INTO event (competition_id, event_type, event_name) VALUES (%s,%s,%s)"
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            'league_round', 'test competition 1 round 1'])
    pytest_setup_vars['testcompetition1_round1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague1_id'],
                            'league_round', 'test competition 1 round 2'])
    pytest_setup_vars['testcompetition1_round2_id'] = cur.lastrowid
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            'league_round', 'test competition 2 round 1'])
    pytest_setup_vars['testcompetition2_round1_id'] = cur.lastrowid
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            'league_round', 'test competition 2 round 2'])
    pytest_setup_vars['testcompetition2_round2_id'] = cur.lastrowid
    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            'league_round', 'test competition 2 round 3'])
    pytest_setup_vars['testcompetition2_round3_id'] = cur.lastrowid

    cur = db.exec_sql(sql, [pytest_setup_vars['testleague2_id'],
                            'league_adjust', 'test competition 2 adjustment'])
    pytest_setup_vars['testcompetition2_adjustment_id'] = cur.lastrowid

    cur = db.exec_sql(
        sql, [pytest_setup_vars['testtournament1_id'], 'poule', 'test poule 1'])
    pytest_setup_vars['testpoule1_id'] = cur.lastrowid
    cur = db.exec_sql(
        sql, [pytest_setup_vars['testtournament1_id'], 'knockout', 'test knockout 1'])
    pytest_setup_vars['testknockout1_id'] = cur.lastrowid

    # matches
    sql = '''
        INSERT INTO `match` (
            `event_id`, `match_start`, `match_date_round`, `match_type`,
            `player_1_id`, `player_1_id_orig`,
            `player_1_score`, `player_1_180s`, `player_1_lollies`,
            `player_2_id`, `player_2_id_orig`,
            `player_2_score`, `player_2_180s`, `player_2_lollies`
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    '''

    cur = db.exec_sql(sql, [
        pytest_setup_vars['testcompetition1_round1_id'],
        '2010-01-01', '1', 'bo3games',
        pytest_setup_vars['player1_id'],
        pytest_setup_vars['player1_id'],
        1, 3, 5,
        pytest_setup_vars['player2_id'],
        pytest_setup_vars['player2_id'],
        2, 4, 6
    ]
    )
    pytest_setup_vars['match1_id'] = cur.lastrowid

    cur = db.exec_sql(sql, [
        pytest_setup_vars['testcompetition1_round1_id'],
        '2010-01-01', '1', 'bo3games',
        pytest_setup_vars['player2_id'],
        pytest_setup_vars['player2_id'],
        2, None, None,
        pytest_setup_vars['player3_id'],
        pytest_setup_vars['player3_id'],
        2, None, None
    ]
    )
    pytest_setup_vars['match2_id'] = cur.lastrowid

    cur = db.exec_sql(sql, [
        pytest_setup_vars['testcompetition1_round1_id'],
        '2010-01-01', '1', 'bo3games',
        pytest_setup_vars['player3_id'],
        pytest_setup_vars['player3_id'],
        2, None, None,
        pytest_setup_vars['player1_id'],
        pytest_setup_vars['player1_id'],
        2, None, None
    ]
    )
    pytest_setup_vars['match3_id'] = cur.lastrowid

    pytest.setup_vars = pytest_setup_vars


def empty_db():
    # clear the database for tests
    cur = db.get_cursor()

    db.exec_sql("DELETE FROM `group_competition`")
    db.exec_sql("DELETE FROM `group_permission`")
    db.exec_sql("DELETE FROM `user_group`")
    db.exec_sql("DELETE FROM `finish`")
    db.exec_sql("DELETE FROM `match`")
    db.exec_sql("DELETE FROM `event` WHERE event_id>0")
    db.exec_sql("DELETE FROM `group` WHERE group_id>0")
    db.exec_sql("DELETE FROM `player_alias`")
    db.exec_sql("DELETE FROM `competition_player`")
    db.exec_sql("DELETE FROM `player`")
    db.exec_sql("DELETE FROM `usercredential`")
    db.exec_sql("DELETE FROM `user`")
    db.exec_sql("DELETE FROM `competition` WHERE competition_id>0")
    db.exec_sql("DELETE FROM `organisation`")
