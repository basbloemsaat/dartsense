from pprint import pprint
from dartsense import List_C
from dartsense import db

import dartsense.event
import dartsense.player


class Competition:

    def __init__(self, id=0, name='',):
        self.id = id
        self.name = name

        if id and not name:
            sql = "SELECT competition_id, competition_name FROM competition where competition_id=%s LIMIT 1"
            res = db.exec_select(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['competition_name']
            else:
                # id not found? get outta here!
                self.id = -1

    def save(self):
        if self.id:
            # update
            pass
        elif not self.id and self.name:
            # insert new
            sql = '''
                INSERT INTO `competition` ( `competition_name`, `competition_type` )
                VALUES ( %s, 'league' )
            '''

            new_id = db.exec_insert(sql, [self.name])
            self.id = new_id

        return self.id

    def delete(self):
        if self.id:
            # delete from db
            sql = " DELETE FROM `competition` WHERE `competition_id` = %s "
            db.exec_sql(sql, [self.id])

        self.id = 0
        self.name = ''

    def __bool__(self):
        return self.id > 0

    def _get_players(self):
        player_list = dartsense.player.PlayerList(
            filters={'competition': self.id})
        return player_list

    players = property(_get_players)

    def _get_events(self):
        event_list = dartsense.event.EventList()
        return event_list

    events = property(_get_events)


class CompetitionList(List_C):

    def __init__(self, filters={}):
        List_C.__init__(self)
        self.filters = filters

    def _search(self, force=False):
        if force or self._elements == []:
            self._elements = []
            args = []

            sql = '''
                SELECT DISTINCT c.competition_id, c.competition_name 
                FROM 
                    competition c
                    LEFT JOIN competition_player cp ON cp.competition_id=c.competition_id
                WHERE c.competition_id > 0
            '''

            if len(self.filters) > 0:
                if 'player' in self.filters:
                    sql += 'AND cp.player_id=%s '
                    args.append(self.filters['player'])
                if 'organisation' in self.filters:
                    sql += 'AND c.organisation_id=%s '
                    args.append(self.filters['organisation'])

            res = db.exec_select(sql, args)

            for r in res:
                self._elements.append(
                    Competition(id=r['competition_id'], name=r['competition_name']))

    def _get_competitions(self):
        return self.elements

    competitions = property(_get_competitions)


#
