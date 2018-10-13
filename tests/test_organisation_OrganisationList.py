#!/usr/bin/env python3

import os
import pytest
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

import dartsense.organisation


organisation_list = None


def test_organisation_list_init(setup_db):
    organisation_list = dartsense.organisation.OrganisationList()

    assert isinstance(organisation_list, dartsense.organisation.OrganisationList)
    assert len(organisation_list) == 2

    i = 0
    for organisation in organisation_list:
        i = i + 1
        assert isinstance(organisation, dartsense.organisation.Organisation)
    assert i == 2


# def test_organisation_list_filter(setup_db):
#     organisation_list = dartsense.organisation.OrganisationList(
#         filters={'competition': pytest.setup_vars['testleague1_id']}
#     )
#     assert len(organisation_list) == 4


# def test_organisation_list_search(setup_db):
#     organisation_list = dartsense.organisation.OrganisationList(
#         search='organisation 3'
#     )
#     assert len(organisation_list) == 1

#     organisation_list = dartsense.organisation.OrganisationList(
#         filters={'competition': pytest.setup_vars['testleague2_id']},
#         search='organisation 3'
#     )
#     assert len(organisation_list) == 1
