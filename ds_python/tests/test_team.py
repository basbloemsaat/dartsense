#!/usr/bin/env python3

import pytest
from dartsense.team import Team
from dartsense.player import Player


def test_team_init():
    team = Team()

    assert team
    assert isinstance(team, Team)


def test_team_players():
    team = Team()

    assert not team.players

    test_player1 = Player(name="test 1")
    team.add_player(test_player1)

    assert team.players
    assert len(team.players) == 1
    assert isinstance(team.players[0], Player)
    assert team.players[0].name == "test 1"

    for player_name in ['test 3', 'test 2']:
        test_player = Player(name=player_name)
        team.add_player(test_player1)

    assert len(team.players) == 3



