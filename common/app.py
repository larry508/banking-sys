from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import FLASK_SECRET_KEY

db = SQLAlchemy()


def get_db():
    return db

def create_app(db_uri: str):
    app = Flask(__name__, template_folder='../templates', static_folder="../static")
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    CSRFProtect(app)
    db.init_app(app)
    return app
