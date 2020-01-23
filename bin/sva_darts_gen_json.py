#!/usr/bin/env python

import getopt
import os
import pathlib
import re
import sys

import libsvadarts as sva

from pprint import pprint

rootdir = os.path.dirname(os.path.abspath(__file__)) + '/../docs/data/'

def main(argv):

    # per seizoen
    data = {}

    competitions = sva.exec_select_query('''
        SELECT DISTINCT comp
        FROM game
        ORDER BY comp
    ''')
    competitions = [c['comp'] for c in competitions]
    for competition in competitions:
        # pprint(competition)

        data['games'] = sva.exec_select_query('''
            SELECT *
            FROM game
            WHERE comp=?
        ''', [competition])

        data['adjustments'] = sva.exec_select_query('''
            SELECT * 
            FROM adjustments a
            where comp=?
        ''', [competition])

        data['standings'] = sva.exec_select_query('''
            SELECT DISTINCT
                x.speler_naam,
                SUM(x.speler_punten) OVER (
                    PARTITION BY x.speler_naam
                    ORDER BY x.game_order ASC
                    RANGE BETWEEN UNBOUNDED PRECEDING AND 
                    UNBOUNDED FOLLOWING
                ) AS speler_punten,
                SUM(x.speler_games) OVER (
                    PARTITION BY x.speler_naam
                    ORDER BY x.game_order ASC
                    RANGE BETWEEN UNBOUNDED PRECEDING AND 
                    UNBOUNDED FOLLOWING
                ) AS speler_games,
                LAST_VALUE ( x.speler_rating ) OVER (
                    PARTITION BY x.speler_naam
                    ORDER BY x.game_order ASC
                    RANGE BETWEEN UNBOUNDED PRECEDING AND 
                    UNBOUNDED FOLLOWING
                ) AS rating 
            FROM (
                SELECT
                    a.comp,
                    0 as game_order,
                    a.speler_naam,
                    a.speler_points as speler_punten,
                    0 as speler_rating,
                    a.speler_games
                FROM adjustments a
                WHERE comp=?
                UNION ALL
                SELECT 
                    g.comp,
                    g.game_order,
                    gd.speler_naam,
                    gd.speler_punten,
                    gd.speler_rating,
                    1 as speler_games
                FROM game g
                JOIN game_data gd on gd.game_id=g.game_id
                WHERE comp=?
            ) as x
            ORDER BY speler_punten DESC

        ''', [competition, competition])

        filename = rootdir + '/perseason/' + competition + '.json'
        # pprint(filename)

        # pprint(data)
        sva.save_data_to_json(data, filename)

    # per speler
    data = {}
    spelers = sva.exec_select_query('''
        SELECT speler_naam
        FROM speler
        ORDER BY speler_naam
    ''')
    spelers = [s['speler_naam'] for s in spelers]
    for speler in spelers:
        pprint(speler)

        filename = rootdir + '/perspeler/' + speler + '.json'
        pprint(filename)
        #TODO

    # overzicht
    data = {}

    data['spelers'] = spelers
    data['competitions'] = competitions

    # pprint(data)

    sva.save_data_to_json(data, rootdir + '/index.json')




def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
