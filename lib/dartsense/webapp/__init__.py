from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask_session import Session
from dartsense import config
import os
static_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../../var/www/static"))

app = Flask(__name__, static_folder=static_folder)
app.wsgi_app = ProxyFix(app.wsgi_app)

if config.session_type == 'dev':
    SESSION_TYPE = 'filesystem'
else:
    SESSION_TYPE = 'redis'

SESSION_COOKIE_NAME = 'dartsense_session'
app.config.from_object(__name__)
Session(app)

from dartsense.webapp import views
