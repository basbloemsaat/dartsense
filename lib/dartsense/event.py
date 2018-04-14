from dartsense import db, List_C

import dartsense.competition
#TODO: link back to competition

class Event:

    def __init__(self, id=None, name=None, type=None):
        self._id = id
        self._type = type
        self.name = None

        if self._id and not self._type:
            sql = '''
                SELECT 
                    e.event_id, e.competition_id, e.event_type, e.event_name
                FROM `event` e
                WHERE 
                    e.event_id=%s
                LIMIT 1
            '''

            res = db.exec_select(sql, [id])

            if(len(res) > 0):
                r = res[0]
                self.name = r['event_name']
                self._type = r['event_type']

            if self._type == 'league_round':
                self.__class__ = LeagueRound
            elif self._type == 'league_adjust':
                self.__class__ = LeagueAdjust
            elif self._type == 'poule':
                self.__class__ = Poule
            elif self._type == 'knockout':
                self.__class__ = Knockout

    def _get_id(self):
        return self._id

    id = property(_get_id)

    def _get_type(self):
        return self._type

    type = property(_get_type)


class LeagueRound(Event):

    def __init__(self, id=None, name=None):
        super(LeagueRound, self).__init__(name=name, type='league_round')


class LeagueAdjust(Event):

    def __init__(self, id=None, name=None):
        super(LeagueAdjust, self).__init__(name=name, type='league_adjust')


class Poule(Event):

    def __init__(self, id=None, name=None):
        super(Poule, self).__init__(name=name, type='poule')


class Knockout(Event):

    def __init__(self, id=None, name=None):
        super(Knockout, self).__init__(name=name, type='knockout')


class EventList(List_C):

    def __init__(self, filters={}):
        List_C.__init__(self)
        self._filters = filters

    def _search(self, force=False):
        if force or self._elements == []:
            self._elements = []
            args = []

            sql = '''
                SELECT DISTINCT 
                    e.event_id
                    , e.competition_id
                    , e.event_type
                    , e.event_name
                FROM event e
                WHERE 1=1
            '''

            if len(self._filters) > 0:
                if 'competition' in self._filters:
                    sql += ' AND e.competition_id=%s '
                    args.append(self._filters['competition'])


            res = db.exec_select(sql, args)

            for r in res:
                self._elements.append(Event(
                    id=r['event_id'],
                    name=r['event_name'],
                    type=r['event_type'],
                ))


#
