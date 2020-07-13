import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'VERY_LONG_SECRET_KEY'

    # RECAPTCHA_PUBLIC_KEY
    # RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'VERY-LONG-RECAPTCHA-PUBLIC-KEY'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or '6LdGxbAZAAAAAFqYgOfa2diM8CJZHy2MxM9-FCet'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'VERY-LONG-RECAPTCHA_PRIVATE_KEY'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
