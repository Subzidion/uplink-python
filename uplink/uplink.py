import os

from flask import Flask, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import createDatabase

from models import Generation, Rank, Division, Merit, Personnel, PersonnelAccount, PersonnelEnlistment

@app.route('/generation', methods=['GET'])
def getGeneration():
    generations = Generation.query.all()
    return jsonify({'generations': [generation.to_dict() for generation in generations]})


@app.route('/generation/<int:id>', methods=['GET'])
def getGenerationByID(id):
    generation = Generation.query.get_or_404(id)
    return jsonify({'generation': generation.to_dict() })

@app.route('/rank', methods=['GET'])
def getRank():
    ranks = Rank.query.all()
    return jsonify({'ranks': [rank.to_dict() for rank in ranks]})

@app.route('/rank/<int:id>', methods=['GET'])
def getRankByID(id):
    rank = Rank.query.get_or_404(id)
    return jsonify({'rank': rank.to_dict() })

@app.route('/division', methods=['GET'])
def getDivision():
    divisions = Division.query.all()
    return jsonify({'divisions': [division.to_dict() for division in divisions]})

@app.route('/division/<int:id>', methods=['GET'])
def getDivisionByID(id):
    division = Division.query.get_or_404(id)
    return jsonify({'division': division.to_dict() })

@app.route('/personnel/<int:id>', methods=['GET'])
def getPersonnelByID(id):
    personnel = Personnel.query.get_or_404(id)
    return jsonify({'personnel': personnel.to_dict() })

@app.route('/personnel/<username>', methods=['GET'])
def getPersonnelByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    return jsonify({'personnel': personnel.to_dict() })

@app.route('/account/<int:id>', methods=['GET'])
def getAccountByID(id):
    account = PersonnelAccount.query.get_or_404(id)
    return jsonify({'account': account.to_dict() })

@app.route('/account/<username>', methods=['GET'])
def getAccountByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    return jsonify({'account': account.to_dict() })

@app.route('/merit/<int:id>', methods=['GET'])
def getMeritByID(id):
    merit = Merit.query.get_or_404(id)
    return jsonify({'merit': merit.to_dict() })

@app.route('/enlistment/<int:id>', methods=['GET'])
def getEnlistmentByID(id):
    enlistment = PersonnelEnlistment.query.get_or_404(id)
    return jsonify({'enlistment': enlistment.to_dict() })

@app.errorhandler(404)
def resourceNotFound(e):
    return jsonify({'error': 'Resource Not Found.'})

@app.errorhandler(400)
def resourceNotFound(e):
    return jsonify({'error': 'Bad Request.'})

if __name__ == '__main__':
    db.create_all()
    app.run()
