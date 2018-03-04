#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../etc/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../lib/"))
os.environ["DARTSENSE_ENV"] = "DEV"

from dartsense.webapp import app

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
app.jinja_env.cache = {}
app.jinja_env.auto_reload = True

try:
    port = int(sys.argv[1])
except (IndexError, ValueError):
    port = 5897

app.run('0.0.0.0', port=port, debug=True,)
