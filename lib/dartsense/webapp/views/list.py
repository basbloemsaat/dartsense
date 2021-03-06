from flask import render_template, jsonify, g

from dartsense.webapp import app
from dartsense.webapp import helpers
from dartsense.competition import Competition
from dartsense.competition import CompetitionList
from dartsense.organisation import Organisation
from dartsense.organisation import OrganisationList
from dartsense.player import Player
from dartsense.event import Event


from pprint import pprint
from dumper import dump
from functools import wraps

def check_access(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not helpers.check_user_permission('ROOT'):
            return "no access", 401
        else:
            return f(*args, **kwargs)

    return wrapper

@app.route('/list/')
@app.route('/list')
@check_access
def list_index():
    return render_template('list/index.j2html')


@app.route('/list/competitions/')
@app.route('/list/competition/')
@app.route('/list/competitions')
@app.route('/list/competition')
@check_access
def list_competitions():
    competition_list = CompetitionList()
    return render_template('list/competitions.j2html', competitions=competition_list)


@app.route('/list/competition/<int:competition_id>')
@check_access
def list_competition(competition_id):
    competition = Competition(id=competition_id)
    return render_template('list/competition.j2html', competition=competition), 200 if competition else 404


@app.route('/list/player/<int:player_id>')
@check_access
def list_player(player_id):
    player = Player(id=player_id)
    return render_template('list/player.j2html', player=player), 200 if player else 404


@app.route('/list/organisations/')
@app.route('/list/organisation/')
@app.route('/list/organisations')
@app.route('/list/organisation')
@check_access
def list_organisations():
    organisation_list = OrganisationList()

    return render_template('list/organisations.j2html', organisations=organisation_list)


@app.route('/list/organisation/<int:organisation_id>')
@check_access
def list_organisation(organisation_id):
    organisation = Organisation(id=organisation_id)
    return render_template('list/organisation.j2html', organisation=organisation), 200 if organisation else 404


@app.route('/list/event/<int:event_id>')
@check_access
def list_event(event_id):
    event = Event(id=event_id)
    return render_template('list/event.j2html', event=event), 200 if event else 404
