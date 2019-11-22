#!/usr/bin/env python
import os
import sys
from pprint import pprint;

from flask import Flask
app = Flask(__name__)

sys.path.append(os.path.join(os.path.dirname(__file__), "../etc/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/"))
os.environ["DARTSENSE_ENV"] = "DEV"
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['DEBUG'] = True
# app.debug = True
# app.jinja_env.cache = {}
# app.jinja_env.auto_reload = True

# pprint(os.path.abspath(os.path.join(os.path.dirname(__file__), "../var/www/static")));
# relpath = os.path.join(os.path.dirname(__file__), "../var/www/static")
# pprint(relpath)
# abspath = os.path.abspath(relpath)
# pprint(abspath)
# # app.static_folder = abspath;
# app.config['STATIC_FOLDER'] = abspath

pprint(app.config)

# @app.route("/static")
# def static_root():
#     return "static page"

# @app.route("/static/<path:subpath>")
# def static_path(subpath):
#     return "static subpath page"

@app.route("/")
def hello():
    return "Hello World!"

try:
    port = int(sys.argv[1])
except (IndexError, ValueError):
    port = 5897

app.run('0.0.0.0', port=port, debug=True,)




