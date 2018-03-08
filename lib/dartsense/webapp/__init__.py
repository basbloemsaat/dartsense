from flask import Flask
from flask_session import Session

from dartsense import config

app = Flask(__name__)
SESSION_TYPE = 'redis'
SESSION_COOKIE_NAME = 'dartsense_session'
app.config.from_object(__name__)
Session(app)

from dartsense.webapp import views

