from dartsense.webapp import app
from dartsense import config
from flask import redirect, url_for, request, render_template, jsonify, g, session
from flask_oauthlib.client import OAuth

from pprint import pprint

oauth = OAuth(app)
oauth_apps = {}
for key in config.oauth2:
    oauth_apps[key] = oauth.remote_app(
        key,
        consumer_key=config.oauth2[key]['consumer_key'],
        consumer_secret=config.oauth2[key]['consumer_secret'],
        request_token_params=config.oauth2[key]['request_token_params'],
        base_url=config.oauth2[key]['base_url'],
        request_token_url=config.oauth2[key]['request_token_url'],
        access_token_method=config.oauth2[key]['access_token_method'],
        access_token_url=config.oauth2[key]['access_token_url'],
        authorize_url=config.oauth2[key]['authorize_url'],
    )


@app.route('/user/')
@app.route('/user')
def user_index():
    session['test'] = 'bla2'
    session['test2'] = 'bla3'

    return render_template('user.j2html')

@app.route('/user/login/<provider>')
def login(provider):

    return provider
