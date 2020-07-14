from flask import Flask
from config import Config

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login = LoginManager(app)
# location of login
login.login_view = 'login'
login.login_message = 'You must login to access this page!'
login.login_message_category = 'info'

app.config.from_object(Config)

from app.routes import *




