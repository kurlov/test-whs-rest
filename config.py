import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres://postgres:pass@localhost:5432/wmsdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
