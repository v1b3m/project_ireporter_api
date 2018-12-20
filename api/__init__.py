from flask import Flask

# def create_app(config_class=Config):
app = Flask(__name__)

from api import routes