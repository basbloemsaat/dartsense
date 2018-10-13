import hashlib

from dartsense import db, List_C
import dartsense.competition


class Organisation:

    def __init__(self, id=0, name=''):
        self.id = id
        self.name = name

        if id and not name:
            sql = '''
                SELECT o.organisation_name
                FROM organisation o
                WHERE o.organisation_id = %s 
                LIMIT 1
            '''

            res = db.exec_select(sql, [id])

            if(len(res) > 0):
                self.name = res[0]['organisation_name']

    def _get_competitions(self):
        competition_list = dartsense.competition.CompetitionList(filters={'organisation': self.id})
        return competition_list

    competitions = property(_get_competitions)


class OrganisationList(List_C):

    def __init__(self, filters={}, search=""):
        List_C.__init__(self)
        self._filters = filters

    def _search(self, force=False):
        if force or self._elements == []:
            self._elements = []
            args = []

            sql = '''
                SELECT
                    o.organisation_id
                    , o.organisation_name
                FROM
                    organisation o
                WHERE 
                    o.organisation_id > 0
            '''

            res = db.exec_select(sql, args)

            for r in res:
                self._elements.append(Organisation(
                    id=r['organisation_id'],
                    name=r['organisation_name'],
                ))

    def _get_organisations(self):
        return self.elements
    organisations = property(_get_organisations)