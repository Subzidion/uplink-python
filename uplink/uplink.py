import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import createDatabase

from models import Generation, Rank, Division, Merit, Personnel, PersonnelAccount, PersonnelEnlistment

@app.route('/')
def index():
    return "Index"

@app.route('/generation/<int:id>')
def generationByID(id):
    generation = Generation.query.get_or_404(id)
    return jsonify({'generation': generation.to_dict() })

@app.route('/rank/<int:id>')
def rankByID(id):
    rank = Rank.query.get_or_404(id)
    return jsonify({'rank': rank.to_dict() })

@app.route('/division/<int:id>')
def divisionByID(id):
    division = Division.query.get_or_404(id)
    return jsonify({'division': division.to_dict() })

@app.route('/personnel/<int:id>')
def personnelByID(id):
    personnel = Personnel.query.get_or_404(id)
    return jsonify({'personnel': personnel.to_dict() })

@app.route('/account/<int:id>')
def accountByID(id):
    account = PersonnelAccount.query.get_or_404(id)
    return jsonify({'account': account.to_dict() })

@app.route('/merit/<int:id>')
def meritByID(id):
    merit = Merit.query.get_or_404(id)
    return jsonify({'merit': merit.to_dict() })

@app.route('/enlistment/<int:id>')
def enlistmentByID(id):
    enlistment = PersonnelEnlistment.query.get_or_404(id)
    return jsonify({'enlistment': enlistment.to_dict() })

@app.errorhandler(404)
def resourceNotFound(e):
    return jsonify({'error': 'Resource Not Found.'})

if __name__ == '__main__':
    db.create_all()
    app.run()
