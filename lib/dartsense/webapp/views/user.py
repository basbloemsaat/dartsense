from flask import redirect, url_for, redirect, request, render_template, jsonify, g, session
from flask_oauthlib.client import OAuth

from dartsense.webapp import app
from dartsense import config
from dartsense.user import User


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
    if 'DEV_SERVER' in app.config and app.config['DEV_SERVER']:
        # make sure there is no user with id=0 in prod!
        session['user_id'] = 0

    if (not 'user_id' in session or session['user_id'] == -1):
        return redirect(url_for('user_login', _external=True, _scheme='https'), code=302)
    else:
        return render_template('user.j2html')


@app.route('/user/login/')
@app.route('/user/login')
def user_login():
    return render_template('user_login.j2html')


@app.route('/user/logout/')
@app.route('/user/logout')
def user_logout():
    session['user_id'] = -1
    return redirect(url_for('user_login', _external=True, _scheme='https'), code=302)


@app.route('/user/login/<provider>')
def login(provider):
    session['current_provider'] = provider
    return oauth_apps[provider].authorize(callback=url_for('authorized', _external=True, _scheme='https'))


@app.route('/user/auth')
def authorized():
    resp = oauth_apps[session['current_provider']].authorized_response()

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session[session['current_provider'] +
            '_token'] = (resp['access_token'], '')

    me = oauth_apps[session['current_provider']].get('userinfo')

    user = User()
    user.login(session['current_provider'], me.data['email'])
    session['user_id'] = user.id
    return redirect(url_for('user_index', _external=True, _scheme='https'), code=302)
    # return jsonify({"data": me.data})
