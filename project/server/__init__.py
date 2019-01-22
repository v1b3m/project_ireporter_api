""" This script will convert the api to a model """
import os

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

bcrypt = Bcrypt(app)

from project.server.incidents import views
from project.server.incidents.views import incident_blueprint
from project.server.auth.views import auth_blueprint

app.register_blueprint(incident_blueprint)
app.register_blueprint(auth_blueprint)
