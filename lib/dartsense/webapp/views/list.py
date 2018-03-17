from flask import render_template, jsonify, g

from dartsense.webapp import app
from dartsense.league import League
from dartsense.league import LeagueList


@app.route('/list/')
@app.route('/list')
def list_index():
    return "list page"


@app.route('/list/leagues/')
@app.route('/list/leagues')
def list_leagues():
    league_list = LeagueList()
    return render_template('list/leagues.j2html', leagues=league_list)


@app.route('/list/league/<league_id>')
def list_league(league_id):
    league = League(league_id)
    return render_template('list/league.j2html', league=league)
