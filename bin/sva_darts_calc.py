#!/usr/bin/env python

import re
import os
import sys

import libsvadarts as sva

from pprint import pprint


def finishes_points(f):
    if(f=='0'):
        return 0

    retval = 0
    finishes = f.split(',')
    for finish in finishes:
        finish = int(finish)
        if finish >= 100 and finish <= 110:
            retval += 1
        elif finish <= 120:
            retval += 2
        elif finish <= 130:
            retval += 3
        elif finish <= 140:
            retval += 4
        elif finish <= 150:
            retval += 5
        elif finish <= 160:
            retval += 6
        elif finish == 161:
            retval += 7
        elif finish == 164:
            retval += 8
        elif finish == 167:
            retval += 9
        elif finish == 170:
            retval += 10
    return retval

def main(argv):
    spelers_a = sva.exec_select_query('''
        SELECT speler_naam, 1000 as rating, 0 as games FROM speler
    ''')
    spelers = {speler['speler_naam']:speler for speler in spelers_a}

    competitions = sva.exec_select_query('''
        SELECT DISTINCT comp
        FROM game
        ORDER BY comp
    ''')
    for competition in competitions:
        comp = competition['comp']
        comp_games = []
        comp_spelers = {}

        # haal de data op van alle games
        games = sva.exec_select_query('''
            SELECT game_id, datum, 
                speler1_naam, speler1_legs, speler1_finishes, speler1_180s, 
                speler2_naam, speler2_legs, speler2_finishes, speler2_180s
            FROM game
            WHERE comp=?
            ORDER BY datum, game_order
        ''',[comp])

        # bereken de punten

        for game in games:
            # pprint(game)
            speler1_punten = 0
            speler2_punten = 0
            if game['speler1_legs'] == 2 and game['speler2_legs'] == 0:
                speler1_punten = 5
            elif game['speler1_legs'] == 2 and game['speler2_legs'] == 1:
                speler1_punten = 3
                speler2_punten = 1
            elif game['speler1_legs'] == 1 and game['speler2_legs'] == 2:
                speler1_punten = 1
                speler2_punten = 3
            elif game['speler1_legs'] == 0 and game['speler2_legs'] == 2:
                speler2_punten = 5

            speler1_punten = speler1_punten + game['speler1_180s']     


            speler1_punten = speler1_punten + finishes_points(game['speler1_finishes'])

            speler2_punten = speler2_punten + game['speler2_180s'] 
            speler2_punten = speler2_punten + finishes_points(game['speler2_finishes'])

            # pprint(str(speler1_punten) + '-' + str(speler2_punten))

        # bereken de rating

    print('---')


if __name__ == "__main__":
    main(sys.argv[1:])