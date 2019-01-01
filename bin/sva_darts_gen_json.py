#!/usr/bin/env python

import getopt
import os
import re
import sys

import libsvadarts as sva

from pprint import pprint

rootdir = '~/src/dartsense/docs/data/'


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
        pprint(competition)

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
                LAST_VALUE ( x.speler_rating ) OVER (
                    PARTITION BY x.speler_naam
                    ORDER BY x.game_order ASC
                    RANGE BETWEEN UNBOUNDED PRECEDING AND 
                    UNBOUNDED FOLLOWING
                ) AS rating 
            FROM (
                SELECT 
                    g.comp,
                    g.game_order,
                    gd.speler_naam,
                    gd.speler_punten,
                    gd.speler_rating
                FROM game g
                JOIN game_data gd on gd.game_id=g.game_id
                WHERE comp=?
                UNION ALL
                SELECT
                    a.comp,
                    0,
                    a.speler_naam,
                    a.speler_points,
                    0
                FROM adjustments a
                WHERE comp=?
            ) as x
            ORDER BY speler_punten DESC

        ''', [competition, competition])

        filename = rootdir + '/perseason/' + competition + '.json'
        pprint(filename)

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

        #TODO

    # overzicht
    data = {}

    data['spelers'] = spelers
    data['competitions'] = competitions

    pprint(data)

    sva.save_data_to_json(data, rootdir + '/index.json')




def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
