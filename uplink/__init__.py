import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from . import models

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .uplink import main
    app.register_blueprint(main)

    from .api import api
    app.register_blueprint(api)

    @app.errorhandler(405)
    def resourceNotFound(e):
        return jsonify({'error': 'Method Not Allowed.'})

    @app.errorhandler(404)
    def resourceNotFound(e):
        return jsonify({'error': 'Resource Not Found.'})

    @app.errorhandler(400)
    def resourceNotFound(e):
        return jsonify({'error': 'Bad Request.'})

    return app
