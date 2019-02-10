import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRETE_KEY = os.environ.get('SECRETE_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # My Own
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True


