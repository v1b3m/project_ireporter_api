import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """ Base Configuration """
    SECRET_KEY = os.getenv('SECRET_KEY', 'very_simple_key')
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    DEBUG=True

class TestingConfig(BaseConfig):
    DEBUG=True
    TESTING = True

class ProductionConfig(BaseConfig):
    SECRET_KEY = 'very_simple_key'
    DEBUG = False