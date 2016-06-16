from flask import jsonify, request, abort

from .. import db
from ..models import Rank

from . import api

@api.route('/rank', methods=['GET'])
def getRanks():
    ranks = Rank.query.all()
    return jsonify({ 'ranks': [ rank.to_dict() for rank in ranks ] })

@api.route('/rank', methods=['POST'])
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

@api.route('/rank/<int:id>', methods=['GET'])
def getRankByID(id):
    rank = Rank.query.get_or_404(id)
    return jsonify({ 'rank': rank.to_dict() })

@api.route('/rank/<int:id>/<attr>', methods=['PUT'])
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
    return jsonify({ attr: data[attr] })

@api.route('/rank/<int:id>/<attr>', methods=['GET'])
def getRankAttrByID(id, attr):
    rank = Rank.query.get_or_404(id)
    try:
        value = getattr(rank, attr)
    except AttributeError:
        abort(404)
    return jsonify({ attr: value })
