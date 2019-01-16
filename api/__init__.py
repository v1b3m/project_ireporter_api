from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig

app = Flask(__name__)
app.config.from_object(TestingConfig)

from api import routes, models