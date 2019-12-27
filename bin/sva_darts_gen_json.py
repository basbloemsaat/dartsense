#!/usr/bin/env python

import getopt
import os
import re
import sys

import libsvadarts as sva

from pprint import pprint

rootdir = '~/src/dartsense/docs/data/'


def main(argv):
    # parameters = {
    #     'filename': '',
    # }

    # try:
    #     opts, args = getopt.getopt(
    #         argv, "hsp:v:",
    #         [
    #             "help", "file="])
    # except getopt.GetoptError as err:
    #     print(err)
    #     usage()

    # for opt, arg in opts:
    #     if opt in ('-h', '--help'):
    #         usage()
    #     elif opt in ("-f", "--file"):
    #         parameters['filename'] = arg

    # if not parameters['filename']:
    #     usage()

    # pprint(parameters)
    # data = sva.load_xlsx(parameters['filename'])

    # # pprint(data)
    # json_filename = re.sub(r'xlsx$', r'json', parameters['filename'])
    # json_filename = re.sub(r'[^/]+/',r'', json_filename)

    # sva.save_data_to_json(data, json_filename)

    # per seizoen

    data = {}

    competitions = sva.exec_select_query('''
        SELECT DISTINCT comp
        FROM game
        ORDER BY comp
    ''')
    for competition in competitions:
        pprint(competition)

        data['games'] = sva.exec_select_query('''
            SELECT *
            FROM game
            WHERE comp=?
        ''', [competition['comp']])

        data['adjustments'] = sva.exec_select_query('''
            SELECT * 
            FROM adjustments a
            where comp=?
        ''', [competition['comp']])

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

        ''', [competition['comp'], competition['comp']])

        filename = rootdir +'/perseason/'+ competition['comp'] + '.json';
        pprint(filename)

        # pprint(data)
        sva.save_data_to_json(data, filename)

    # per speler


def usage():
    print('''read_file.py 
        --file <filename>
        ''')
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
