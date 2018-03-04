from dartsense.webapp import app
from flask import render_template, jsonify, g, session

@app.route('/user/')
@app.route('/user')
def user_index():
    session['test'] = 'bla2'
    session['test2'] = 'bla3'

    return "user page works"