#!/usr/bin/env python

import os
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "../../lib/"))
from dartsense import db

match_list = db.exec_select("""
    SELECT m.player_1_id, m.player_2_id
    FROM `event` e
        LEFT JOIN `match` m ON m.event_id = e.event_id
    WHERE e.competition_id = 6
""")

players = {}

# pprint(match_list)

def player_add_opponent(player_id, opponent_id):
    if not opponent_id in players[player_id]['lookup']:
        new_entry = {
            'opponent_id': opponent_id,
            'nr_matches': 0
        }

        players[player_id]['lookup'][opponent_id] = new_entry
        players[player_id]['sort'].append(new_entry)    


def add_to_players(player_id, opponent_id):
    if not player_id in players:
        players[player_id] = {
            'lookup': {},
            'sort': []
        }

    # if not opponent_id in players[player_id]['lookup']:
    player_add_opponent(player_id, opponent_id)

    players[player_id]['lookup'][opponent_id]['nr_matches'] = players[
        player_id]['lookup'][opponent_id]['nr_matches'] + 1


for match in match_list:
    add_to_players(match['player_1_id'], match['player_2_id'])
    add_to_players(match['player_2_id'], match['player_1_id'])



for player_id in players:
    player_games = players[player_id]

    for opponent_id in players:
        if player_id == opponent_id:
            continue

        player_add_opponent(player_id, opponent_id)


pprint(players)
    # print(players[player_id])
    # newlist =
