
from datetime import datetime, date
from hashlib import sha256

from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

from common.app import create_app
from config import DB_URI
from views import auth_blueprint, customer_blueprint, index_blueprint


    
app = create_app(DB_URI)
app.register_blueprint(index_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(customer_blueprint, url_prefix='/customer')



if __name__ == '__main__':
    app.run()
