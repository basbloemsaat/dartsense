from pprint import pprint
import hashlib

from dartsense import db, List_C
import dartsense.player


class Match:

    def __init__(
        self,
        id=None,
        player1=None,
        player2=None,
    ):
        self._id = id
        self._player1_id = None
        self._player2_id = None

        if id and not (player1 or player2):
            sql = '''
                SELECT 
                    `match_id`, `event_id`, `match_date`, 
                    `match_date_round`, `match_type`,
                    `player_1_id`, `player_1_id_orig`,
                    `player_1_score`, `player_1_180s`, `player_1_lollies`,
                    `player_2_id`, `player_2_id_orig`,
                    `player_2_score`, `player_2_180s`, `player_2_lollies`
                FROM `match` m
                WHERE 
                    m.match_id = %s
                LIMIT 1
            '''

            res = db.exec_sql(sql, [id])

            if(len(res) > 0):
                r = res[0]
                self._player1_id = r['player_1_id']
                self._player2_id = r['player_2_id']

    def _get_id(self):
        return self._id

    id = property(_get_id)

    def _get_player_1(self):
        return self._get_player(1)

    def _get_player_2(self):
        return self._get_player(2)

    def _get_player(self, nr):
        return getattr(self, '_player' + str(nr) + '_id')

    player_1 = property(_get_player_1)
    player_2 = property(_get_player_2)


# class PlayerList(List_C):

#     def __init__(self, filters={}, search=""):
#         List_C.__init__(self)
#         self._filters = filters
#         self._searchstr = search

#     def _search(self, force=False):
#         if force or self._elements == None:
#             self._elements = []
#             args = []

#             sql = '''
#                 SELECT DISTINCT p.*
#                 FROM player p
#                     LEFT JOIN competition_player lp ON lp.player_id=p.player_id
#                 WHERE 1=1
#             '''

#             if len(self._filters) > 0:
#                 if 'competition' in self._filters:
#                     sql += 'AND lp.competition_id=%s '
#                     args.append(self._filters['competition'])

#             if self._searchstr:
#                 sql += 'AND p.player_name LIKE %s'
#                 args.append('%' + self._searchstr + '%')

#             res = db.exec_sql(sql, args)

#             for r in res:
#                 self._elements.append(Player(
#                     id=r['player_id'],
#                     name=r['player_name'],
#                     nickname=r['player_nickname'],
#                 ))

#     def add_player(self, player):
#         self.self._elements[player.id] = player

#     def _get_players(self):
#         return self.elements
#     players = property(_get_players)
