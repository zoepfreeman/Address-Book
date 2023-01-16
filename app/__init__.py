
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# Create an instance of LoginManager to set up login functionality
login = LoginManager(app)

# import all of the routes from the routes file into the current folder
from . import routes, models

