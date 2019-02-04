""" This script will convert the api to a model """
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from flasgger import Swagger

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)

app.config.from_object(app_settings)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

bcrypt = Bcrypt(app)
Swagger(app)

from project.server.interventions.views import interventions_blueprint
from project.server.auth.views import auth_blueprint
from project.server.redflags.views import redflags_blueprint

app.register_blueprint(redflags_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(interventions_blueprint)
