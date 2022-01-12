from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_URI


db = SQLAlchemy()


def create_app(db_uri: str):
    app = Flask(__name__, template_folder='../templates', static_folder="../static")
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    return app
