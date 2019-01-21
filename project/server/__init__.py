""" This script will convert the api to a model """
from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

from project.server.incidents import views
from project.server import models
