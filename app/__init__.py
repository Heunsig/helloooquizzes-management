import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfasdfkaf;kjs;fasdfajds;fl'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:D8t44m5b@#@localhost:5432/vocab_quiz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

IS_PROD = os.environ.get('IS_HEROKU', None)

if IS_PROD:
    os.environ['WEB_PATH'] = os.environ.get('WEB_PATH_PROD', None)
else:
    os.environ['WEB_PATH'] = 'http://127.0.0.1:5000'
