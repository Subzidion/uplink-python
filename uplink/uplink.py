import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import createDatabase

from models import Generation, Rank, Division, Merit, Personnel, PersonnelAccount, PersonnelEnlistment

@app.route('/', methods=['GET'])
def getIndex():
    return jsonify({
        'generations': 'https://uplink.subzidion.co/generation',
        'generation': 'https://uplink.subzidion.co/generation/<id>',
        'ranks': 'https://uplink.subzidion.co/rank',
        'rank': 'https://uplink.subzidion.co/rank/<id>',
        'divisions': 'https://uplink.subzidion.co/division',
        'division': 'https://uplink.subzidion.co/division/<id>',
        'merits': 'https://uplink.subzidion.co/merit',
        'merit': 'https://uplink.subzidion.co/merit/<id>',
        'account': 'https://uplink.subzidion.co/account/<id>',
        'account': 'https://uplink.subzidion.co/account/<username>',
        'personnel': 'https://uplink.subzidion.co/personnel/<pid>',
        'personnel': 'https://uplink.subzidion.co/personnel/<username>'
        })


@app.route('/generation', methods=['GET'])
def getGenerations():
    generations = Generation.query.all()
    return jsonify({'generations': [generation.to_dict() for generation in generations]})

@app.route('/generation', methods=['POST'])
def postGeneration():
    if not request.json:
        abort(400)
    data = request.json
    try:
        generation = Generation(name=data['name'], description=data['description'], textureUUID=data['textureUUID'])
    except KeyError:
        abort(400)
    db.session.add(generation)
    db.session.commit()
    r = jsonify(generation.to_dict())
    r.status_code = 201
    return r

@app.route('/generation/<int:id>', methods=['GET'])
def getGenerationByID(id):
    generation = Generation.query.get_or_404(id)
    return jsonify({'generation': generation.to_dict() })

@app.route('/generation/<int:id>/<attr>', methods=['GET'])
def getGenerationAttrByID(id, attr):
    generation = Generation.query.get_or_404(id)
    try:
        value = getattr(generation, attr)
    except AttributeError:
        abort(404)
    return jsonify({attr: value })

@app.route('/generation/<int:id>/<attr>', methods=['PUT'])
def putGenerationAttrByID(id, attr):
    if not hasattr(Generation, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    generation = Generation.query.get_or_404(id)
    try:
        setattr(generation, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({attr: data[attr] })


@app.route('/rank', methods=['GET'])
def getRanks():
    ranks = Rank.query.all()
    return jsonify({'ranks': [rank.to_dict() for rank in ranks]})

@app.route('/rank', methods=['POST'])
def postRank():
    if not request.json:
        abort(400)
    data = request.json
    try:
        rank = Rank(name=data['name'], description=data['description'], textureUUID=data['textureUUID'])
    except KeyError:
        abort(400)
    db.session.add(rank)
    db.session.commit()
    r = jsonify(rank.to_dict())
    r.status_code = 201
    return r

@app.route('/rank/<int:id>', methods=['GET'])
def getRankByID(id):
    rank = Rank.query.get_or_404(id)
    return jsonify({'rank': rank.to_dict() })

@app.route('/rank/<int:id>/<attr>', methods=['PUT'])
def putRankAttrByID(id, attr):
    if not hasattr(Rank, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    rank = Rank.query.get_or_404(id)
    try:
        setattr(rank, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({attr: data[attr] })

@app.route('/rank/<int:id>/<attr>', methods=['GET'])
def getRankAttrByID(id, attr):
    rank = Rank.query.get_or_404(id)
    try:
        value = getattr(rank, attr)
    except AttributeError:
        abort(404)
    return jsonify({attr: value })



@app.route('/division', methods=['GET'])
def getDivisions():
    divisions = Division.query.all()
    return jsonify({'divisions': [division.to_dict() for division in divisions]})

@app.route('/division', methods=['POST'])
def postDivision():
    if not request.json:
        abort(400)
    data = request.json
    try:
        division = Division(name=data['name'], description=data['description'], textureUUID=data['textureUUID'])
    except KeyError:
        abort(400)
    db.session.add(division)
    db.session.commit()
    r = jsonify(division.to_dict())
    r.status_code = 201
    return r

@app.route('/division/<int:id>', methods=['GET'])
def getDivisionByID(id):
    division = Division.query.get_or_404(id)
    return jsonify({'division': division.to_dict() })

@app.route('/division/<int:id>/<attr>', methods=['PUT'])
def putDivisionAttrByID(id, attr):
    if not hasattr(Division, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    division = Division.query.get_or_404(id)
    try:
        setattr(division, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({attr: data[attr] })

@app.route('/division/<int:id>/<attr>', methods=['GET'])
def getDivisionAttrByID(id, attr):
    division = Division.query.get_or_404(id)
    try:
        value = getattr(division, attr)
    except AttributeError:
        abort(404)
    return jsonify({attr: value })



@app.route('/merit', methods=['GET'])
def getMerits():
    merits = Merit.query.all()
    return jsonify({'merit': [merit.to_dict() for merit in merits] })

@app.route('/merit', methods=['POST'])
def postMerit():
    if not request.json:
        abort(400)
    data = request.json
    try:
        merit = Merit(name=data['name'], description=data['description'], textureUUID=data['textureUUID'])
    except KeyError:
        abort(400)
    db.session.add(merit)
    db.session.commit()
    r = jsonify(merit.to_dict())
    r.status_code = 201
    return r

@app.route('/merit/<int:id>', methods=['GET'])
def getMeritByID(id):
    merit = Merit.query.get_or_404(id)
    return jsonify({'merit': merit.to_dict() })

@app.route('/merit/<int:id>/<attr>', methods=['PUT'])
def putMeritAttrByID(id, attr):
    if not hasattr(Merit, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    merit = Merit.query.get_or_404(id)
    try:
        setattr(merit, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({attr: data[attr] })

@app.route('/merit/<int:id>/<attr>', methods=['GET'])
def getMeritAttrByID(id, attr):
    merit = Merit.query.get_or_404(id)
    try:
        value = getattr(merit, attr)
    except AttributeError:
        abort(404)
    return jsonify({attr: value })



@app.route('/personnel/<int:id>', methods=['GET'])
def getPersonnelByID(id):
    personnel = Personnel.query.get_or_404(id)
    return jsonify({'personnel': personnel.to_dict() })

@app.route('/personnel/<int:id>/<attr>', methods=['GET'])
def getPersonnelAttrByID(id, attr):
    personnel = Personnel.query.get_or_404(id)
    try:
        value = getattr(personnel, attr)
    except AttributeError:
        abort(404)
    return jsonify({ attr: value })

@app.route('/personnel/<int:id>/<attr>', methods=['PUT'])
def putPersonnelAttrByID(id, attr):
    if not hasattr(Personnel, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    personnel = Personnel.query.get_or_404(id)
    try:
        setattr(personnel, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({ attr: data[attr] })

@app.route('/personnel/<username>', methods=['GET'])
def getPersonnelByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    return jsonify({'personnel': personnel.to_dict() })

@app.route('/personnel/<username>/<attr>', methods=['GET'])
def getPersonnelAttrByUsername(username, attr):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    try:
        value = getattr(personnel, attr)
    except AttributeError:
        abort(404)
    try:
        return jsonify({ attr: [ item.to_dict() for item in value ] })
    except TypeError:
        return jsonify({ attr: value })

@app.route('/personnel/<username>/<attr>', methods=['PUT'])
def putPersonnelAttrByUsername(username, attr):
    if not hasattr(Personnel, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    try:
        setattr(personnel, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({ attr: data[attr] })

@app.route('/account/<int:id>', methods=['GET'])
def getAccountByID(id):
    account = PersonnelAccount.query.get_or_404(id)
    return jsonify({'account': account.to_dict() })

@app.route('/account/<username>/<attr>', methods=['GET'])
def getAccountAttrByID(id, attr):
    account = PersonnelAccount.query.get_or_404(id)
    try:
        value = getattr(account, attr)
    except AttributeError:
        abort(404)
    try:
        return jsonify({ attr: [ item.to_dict() for item in value ] })
    except TypeError:
        return jsonify({ attr: value })

@app.route('/account/<username>/<attr>', methods=['PUT'])
def putAccountAttrByID(id, attr):
    if not hasattr(PersonnelAccount, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    account = PersonnelAccount.query.get_or_404(id)
    try:
        setattr(account, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({ attr: data[attr] })

@app.route('/account/<username>', methods=['GET'])
def getAccountByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    return jsonify({'account': account.to_dict() })


@app.route('/account/<username>/<attr>', methods=['GET'])
def getAccountAttrByUsername(username, attr):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    try:
        value = getattr(account, attr)
    except AttributeError:
        abort(404)
    try:
        return jsonify({ attr: [ item.to_dict() for item in value ] })
    except TypeError:
        return jsonify({ attr: value })

@app.route('/account/<username>/<attr>', methods=['PUT'])
def putAccountAttrByUsername(username, attr):
    if not hasattr(PersonnelAccount, attr):
        abort(404)
    if not request.json or attr == 'id' or attr not in request.json:
        abort(400)
    data = request.json
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    try:
        setattr(account, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({ attr: data[attr] })

@app.errorhandler(405)
def resourceNotFound(e):
    return jsonify({'error': 'Method Not Allowed.'})

@app.errorhandler(404)
def resourceNotFound(e):
    return jsonify({'error': 'Resource Not Found.'})

@app.errorhandler(400)
def resourceNotFound(e):
    return jsonify({'error': 'Bad Request.'})



if __name__ == '__main__':
    app.run()
