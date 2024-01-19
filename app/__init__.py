from app import routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretpass'  # Altere para um valor secreto real
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
