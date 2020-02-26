import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try-and-guess-this'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False