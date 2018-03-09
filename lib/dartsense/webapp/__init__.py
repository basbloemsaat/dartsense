from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask_session import Session

from dartsense import config

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

SESSION_TYPE = 'redis'
SESSION_COOKIE_NAME = 'dartsense_session'
app.config.from_object(__name__)
Session(app)

from dartsense.webapp import views

