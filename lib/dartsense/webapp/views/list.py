from flask import render_template, jsonify, g

from dartsense.webapp import app
from dartsense.competition import Competition
from dartsense.competition import CompetitionList
from dartsense.organisation import OrganisationList
from dartsense.player import Player


from pprint import pprint
from dumper import dump


@app.route('/list/')
@app.route('/list')
def list_index():
    return "list page"


@app.route('/list/competitions/')
@app.route('/list/competition/')
@app.route('/list/competitions')
@app.route('/list/competition')
def list_competitions():
    competition_list = CompetitionList()
    return render_template('list/competitions.j2html', competitions=competition_list)


@app.route('/list/competition/<int:competition_id>')
def list_competition(competition_id):
    competition = Competition(id=competition_id)
    return render_template('list/competition.j2html', competition=competition), 200 if competition else 404


@app.route('/list/player/<int:player_id>')
def list_player(player_id):
    player = Player(id=player_id)
    return render_template('list/player.j2html', player=player), 200 if player else 404


@app.route('/list/organisations/')
@app.route('/list/organisation/')
@app.route('/list/organisations')
@app.route('/list/organisation')
def list_organisations():
    organisation_list = OrganisationList()
    print(len(organisation_list))

    return render_template('list/organisations.j2html', organisations=organisation_list)


