from dartsense import db, List_C

import dartsense.competition
# TODO: link back to competition


class Event:

    def __init__(self, id=None, name=None, type=None, competition=None):
        self._id = id
        self._type = type
        self.name = name

        self._competition_id = None
        self._competition = None


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
                self._competition_id = r['competition_id']

            if self._type == 'league_round':
                self.__class__ = LeagueRound
            elif self._type == 'league_adjust':
                self.__class__ = LeagueAdjust
            elif self._type == 'poule':
                self.__class__ = Poule
            elif self._type == 'knockout':
                self.__class__ = Knockout

        self.competition = competition

    def save(self):
        if self._id:
            sql = """
                UPDATE `event`
                SET 
                    competition_id = %s
                    , event_type = %s
                    , event_name = %s
                WHERE event_id = %s
            """

            db.exec_sql(sql, [
                self._competition_id,
                self._type,
                self.name,
                self._id
            ])
        else:
            if not (
                self._type and
                self._competition_id and
                self.name
            ):
                return None

            sql = """
                INSERT INTO `event` 
                (
                    competition_id
                    , event_type
                    , event_name
                ) VALUES (
                    %s, %s, %s
                )
            """

            new_id = db.exec_insert(
                sql,
                [
                    self._competition_id,
                    self._type,
                    self.name
                ]
            )

            self._id = new_id
            
        return self._id

    def _get_id(self):
        return self._id

    id = property(_get_id)

    def _get_type(self):
        return self._type

    type = property(_get_type)

    def _get_competition(self):
        if self._competition_id and not self._competition:
            self._competition = dartsense.competition.Competition(
                id=self._competition_id)
        return self._competition

    def _set_competition(self, competition):
        if isinstance(competition, dartsense.competition.Competition):
            self._competition = competition
            self._competition_id = competition.id
        elif isinstance(competition, int) and competition > 0:
            self._competition = None
            self._competition_id = competition

    competition = property(_get_competition, _set_competition)


class LeagueRound(Event):

    def __init__(self, id=None, name=None, competition=None):
        super(LeagueRound, self).__init__(
            name=name, type='league_round', competition=competition)


class LeagueAdjust(Event):

    def __init__(self, id=None, name=None, competition=None):
        super(LeagueAdjust, self).__init__(
            name=name, type='league_adjust', competition=competition)


class Poule(Event):

    def __init__(self, id=None, name=None, competition=None):
        super(Poule, self).__init__(
            name=name, type='poule', competition=competition)


class Knockout(Event):

    def __init__(self, id=None, name=None, competition=None):
        super(Knockout, self).__init__(
            name=name, type='knockout', competition=competition)


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
                FROM 
                    event e
                    LEFT JOIN `match` m ON m.event_id=e.event_id
                WHERE 1=1
            '''

            if len(self._filters) > 0:
                if 'competition' in self._filters:
                    sql += ' AND e.competition_id=%s '
                    args.append(self._filters['competition'])

                if 'player' in self._filters:
                    sql += ' AND ( m.player_1_id = %s OR player_1_id = %s ) '
                    args.append(self._filters['player'])
                    args.append(self._filters['player'])

            res = db.exec_select(sql, args)

            for r in res:
                self._elements.append(Event(
                    id=r['event_id'],
                    name=r['event_name'],
                    type=r['event_type'],
                ))


#
