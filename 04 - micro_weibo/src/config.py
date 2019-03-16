import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'A-VERY-LOW-SECRET-KEY'
    RECAPTCHA_PUBLIC_KEY = os.environ.get(
        'RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LOW-RECAPTCHA-PUBLIC-KEY'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'MAIL_USERNAME'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'MAIL_PASSWORD'
