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

