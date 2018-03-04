from dartsense.webapp import app
from flask import render_template, jsonify, g

@app.route('/test/')
@app.route('/test')
def test_index():
    return "test page works"