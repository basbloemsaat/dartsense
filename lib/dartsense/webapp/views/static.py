# serves static files for development purposes

from flask import send_from_directory

from dartsense.webapp import app

from pprint import pprint
from dumper import dump


@app.route('/static/')
@app.route('/static')
def static_index():
    return "static page"


@app.route('/static/<path:filename>')
def send_static(filename):
    # pprint(path)
    pprint(filename)

    return 'meh';

    # return send_from_directory('static', path)
