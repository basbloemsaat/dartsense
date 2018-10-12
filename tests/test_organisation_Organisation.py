#!/usr/bin/env python3

import pytest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.organisation


def test_organisation_init(setup_db):
    organisation = dartsense.organisation.Organisation()
    assert isinstance(organisation, dartsense.organisation.Organisation)

    assert not organisation.name

    organisation = dartsense.organisation.Organisation(name='Test Organisation 1')
    assert isinstance(organisation, dartsense.organisation.Organisation)
    assert organisation.name
    assert organisation.name == 'Test Organisation 1'

def test_organisation_load(setup_db):
    organisation = dartsense.organisation.Organisation(id=pytest.setup_vars['organisation1_id'])
    assert isinstance(organisation, dartsense.organisation.Organisation)
    assert organisation.name == 'Test Organisation 1'

def test_organisation_Competitions(setup_db):
    organisation = dartsense.organisation.Organisation(id=pytest.setup_vars['organisation1_id'])
    assert hasattr(organisation, 'competitions')
    competitions_list = organisation.competitions

    assert isinstance(competitions_list, dartsense.competition.CompetitionList)
    assert len(competitions_list) == 2
    assert isinstance(competitions_list[0],  dartsense.competition.Competition)
    assert competitions_list[0].name == 'test league 1'
    assert competitions_list[1].name == 'test tournament 1'


