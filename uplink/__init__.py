import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from .secrets import SECRET_KEY

db = SQLAlchemy()

def create_app(testing=False):
    app = Flask(__name__)
    app.secret_key = SECRET_KEY 
    basedir = os.path.abspath(os.path.dirname(__file__))
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)
    
    from .uplink import main
    app.register_blueprint(main)

    from .api import api
    app.register_blueprint(api)
    return app
