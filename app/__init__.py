from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# configure app
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.models import User
from app import routes
