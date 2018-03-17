from flask import render_template, jsonify, g

from dartsense.webapp import app
from dartsense.league import LeagueList



@app.route('/list/')
@app.route('/list')
def list_index():
    return "list page"

@app.route('/list/leagues/')
@app.route('/list/leagues')
def list_leagues():
    leaguelist = LeagueList()
    return render_template('list/league.j2html', leagues = leaguelist)