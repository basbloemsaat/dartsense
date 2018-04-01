from dartsense import db, List_C


class Event:
    def __init__(self, id=None, name='', type=None):
        self._id = id
        self._type = type
        self.name = None

        if id and not name:
            sql = '''
                SELECT 
                    e.event_id, e.competition_id, e.event_type, e.event_name
                FROM `event` e
                WHERE 
                    e.event_id=%s
                LIMIT 1
            '''

            res = db.exec_sql(sql, [id])

            if(len(res) > 0):
                r = res[0]
                self.name = r['event_name']
                # if r['event_type'] == 'league_round':
                #     self=LeagueRound()
                # elif r['event_type'] == 'league_adjust':
                #     self=LeagueAdjust()
                # elif r['event_type'] == 'poule':
                #     self=Poule()
                # elif r['event_type'] == 'knockout':
                #     self=Knockout()


        self._id = id

    def _get_id(self):
        return self._id

    def _get_type(self):
        return self._type

    id = property(_get_id)
    type = property(_get_type)


class LeagueRound(Event):

    def __init__(self, id=None, name=''):
        if (id):
            super(LeagueRound, self).__init__(name=name)
            if self._type != 'league_round':
                raise RuntimeError("id is not a LeagueRound")
        else: self._type = 'league_round'


class LeagueAdjust(Event):

    def __init__(self, id=None):
        if (id):
            super(LeagueAdjust, self).__init__(name=name)
            if self._type != 'league_adjust':
                raise RuntimeError("id is not a LeagueAdjust")
        else: self._type = 'league_adjust'


class Poule(Event):

    def __init__(self, id=None):
        if (id):
            super(Poule, self).__init__(name=name)
            if self._type != 'poule':
                raise RuntimeError("id is not a Poule")
        else: self._type = 'poule'


class Knockout(Event):

    def __init__(self, id=None):
        if (id):
            super(Knockout, self).__init__(name=name)
            if self._type != 'knockout':
                raise RuntimeError("id is not a Knockout")
        else: self._type = 'knockout'


class EventList(List_C):

    def __init(self):
        self.list = []
