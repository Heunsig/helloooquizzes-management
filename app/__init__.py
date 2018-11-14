import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_sslify import SSLify

IS_PROD = os.environ.get('IS_HEROKU', None)

WEB_PATH = 'http://127.0.0.1:5000'
DATABASE_URL = 'postgresql://postgres:D8t44m5b@#@localhost:5432/vocab_quiz'
if IS_PROD:
    WEB_PATH = os.environ.get('WEB_PATH', None)
    DATABASE_URL = os.environ.get('DATABASE_URL', None)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfasdfkaf;kjs;fasdfajds;fl'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

sslify = SSLify(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
