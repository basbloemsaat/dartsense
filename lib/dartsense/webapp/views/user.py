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
        **config.oauth2[key]
    )

google = oauth_apps['google']


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


@app.route('/user/')
@app.route('/user')
def user_index():
    return render_template('user.j2html')


@app.route('/user/login/<provider>')
def login(provider):

    # pprint(url_for('authorized', _external=True))
    session['current_provider'] = provider
    # return "" + url_for('authorized', _external=True, _scheme='https');
    return oauth_apps[provider].authorize(callback=url_for('authorized', _external=True, _scheme='https'))


@app.route('/user/auth')
def authorized():
    resp = oauth_apps[session['current_provider']].authorized_response()
    pprint(session['current_provider'])
    pprint(resp)

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session[session['current_provider'] + '_token'] = (resp['access_token'], '')

    me = oauth_apps[session['current_provider']].get('userinfo')
    return jsonify({"data": me.data})
