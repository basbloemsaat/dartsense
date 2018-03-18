from flask import render_template, jsonify, g

from dartsense.webapp import app
from dartsense.league import League
from dartsense.league import LeagueList
from dartsense.player import Player


from pprint import pprint
from dumper import dump


@app.route('/list/')
@app.route('/list')
def list_index():
    return "list page"


@app.route('/list/leagues/')
@app.route('/list/leagues')
def list_leagues():
    league_list = LeagueList()
    return render_template('list/leagues.j2html', leagues=league_list)


@app.route('/list/league/<int:league_id>')
def list_league(league_id):
    league = League(id=league_id)

    return render_template('list/league.j2html', league=league)

@app.route('/list/player/<int:player_id>')
def list_player(player_id):
    player = Player(id=player_id)
    return render_template('list/player.j2html', player=player)