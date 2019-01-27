from pprint import pprint
import hashlib
import datetime

from dartsense import db, List_C
import dartsense.event
import dartsense.player


class Match:

    def __init__(
        self,
        id=None,
        player_1=None,
        player_2=None,
        event=None,
        date=datetime.date.today()
    ):
        self._id = id
        self._player_1_id = None
        self._player_2_id = None
        self._player_1 = None
        self._player_2 = None
        self.player_1 = player_1
        self.player_2 = player_2

        self._event_id = None
        self._event = None
        self.event = event

        self._date = date
        self.round = 0
        self.type = None

        self.player_1_score = 0
        self.player_1_180s = 0
        self.player_1_lollies = 0
        self.player_1_finishes = []

        self.player_2_score = 0
        self.player_2_180s = 0
        self.player_2_lollies = 0
        self.player_2_finishes = []

        if id and not (player_1 or player_2 or event):
            sql = '''
                SELECT 
                    `match_id`, `event_id`, `match_start`, 
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

            res = db.exec_select(sql, [id])

            if(len(res) > 0):
                r = res[0]
                self._player_1_id = r['player_1_id']
                self._player_2_id = r['player_2_id']
                self._event_id = r['event_id']

                self.round = r['match_date_round']
                self.type = r['match_type']

                self.player_1_score = r['player_1_score']
                self.player_1_180s = r['player_1_180s']
                self.player_1_lollies = r['player_1_lollies']

                self.player_2_score = r['player_2_score']
                self.player_2_180s = r['player_2_180s']
                self.player_2_lollies = r['player_2_lollies']

    def save(self):
        if self._id:
            # update
            sql = '''
                UPDATE `match`
                SET
                      `event_id` = %s
                    , `match_start` = %s
                    , `match_date_round` = %s
                    , `match_type` = %s
                    , `player_1_id` = %s
                    , `player_1_score` = %s
                    , `player_1_180s` = %s
                    , `player_1_lollies` = %s
                    , `player_2_id` = %s
                    , `player_2_score` = %s
                    , `player_2_180s` = %s
                    , `player_2_lollies` = %s
                WHERE
                    match_id = %s
            '''

            db.exec_sql(sql, [
                self._event_id,
                self._date,
                self.round,
                self.type,
                self._player_1_id,
                self.player_1_score,
                self.player_1_180s,
                self.player_1_lollies,
                self._player_2_id,
                self.player_2_score,
                self.player_2_180s,
                self.player_2_lollies,
                self._id
            ])
        else:
            if not (
                self._player_1_id and
                self._player_2_id and
                self._event_id
            ):
                return None
            # insert
            sql = '''
                INSERT INTO `match`
                (
                    `event_id`, `match_start`, 
                    `match_date_round`, `match_type`,
                    `player_1_id`, `player_1_id_orig`,
                    `player_1_score`, `player_1_180s`, `player_1_lollies`,
                    `player_2_id`, `player_2_id_orig`,
                    `player_2_score`, `player_2_180s`, `player_2_lollies`
                )
                VALUES
                (
                    %s, %s, 
                    %s, %s, 
                    %s, %s, 
                    %s, %s, %s, 
                    %s, %s, %s, 
                    %s, %s 
                )
            '''

            new_id = db.exec_insert(
                sql,
                [
                    self._event_id,
                    self._date,
                    self.round,
                    self.type,
                    self._player_1_id,
                    self._player_1_id,
                    self.player_1_score,
                    self.player_1_180s,
                    self.player_1_lollies,
                    self._player_2_id,
                    self._player_2_id,
                    self.player_2_score,
                    self.player_2_180s,
                    self.player_2_lollies,
                ]
            )

            self._id = new_id

        return self._id

    def _get_id(self):
        return self._id

    id = property(_get_id)

    def _get_player_1(self):
        return self._get_player(1)

    def _get_player_2(self):
        return self._get_player(2)

    def _set_player_1(self, player):
        return self._set_player(1, player)

    def _set_player_2(self, player):
        return self._set_player(2, player)

    def _get_player(self, nr):
        player = getattr(self, '_player_' + str(nr))
        player_id = getattr(self, '_player_' + str(nr) + '_id')
        if not player and player_id:
            player = dartsense.player.Player(id=player_id)
        return player

    def _set_player(self, nr, player):
        if isinstance(player, dartsense.player.Player):
            setattr(self, '_player_' + str(nr), player)
            setattr(self, '_player_' + str(nr) + '_id', player.id)
        elif isinstance(player, int) and player > 0:
            setattr(self, '_player_' + str(nr), None)
            setattr(self, '_player_' + str(nr) + '_id', player)

    def _get_event(self):
        if not self._event and self._event_id:
            self._event = dartsense.event.Event(id=self._event_id)
        return self._event

    def _set_event(self, event):
        if isinstance(event, dartsense.event.Event):
            self._event = event
            self._event_id = event.id
        elif isinstance(event, int) and event > 0:
            self._event = None
            self._event_id = event

    player_1 = property(_get_player_1, _set_player_1)
    player_2 = property(_get_player_2, _set_player_2)
    event = property(_get_event, _set_event)


class MatchList(List_C):

    def __init__(self, filters={}):
        List_C.__init__(self)
        self._filters = filters

    def _search(self, force=False):
        if force or self._elements == []:
            self._elements = []

            args = []

            sql = """
                SELECT DISTINCT
                    m.match_id
                FROM
                    `match` m
                    LEFT JOIN event e ON e.event_id = m.event_id
                WHERE
                    e.event_id > 0

            """

            if len(self._filters) > 0:
                if 'event' in self._filters:
                    sql += ' AND e.event_id = %s'
                    args.append(self._filters['event'])

            else:
                # a matchlist with no filters would be huge: don't list
                return

            res = db.exec_select(sql, args)
            for r in res:
                self._elements.append(Match(
                    id=r['match_id'],
                ))
