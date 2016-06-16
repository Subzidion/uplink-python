from flask import jsonify, request, abort

from .. import db
from ..models import Generation

from . import api

@api.route('/generation', methods=['GET'])
def getGenerations():
    generations = Generation.query.all()
    return jsonify({ 'generations': [ generation.to_dict() for generation in generations ] })

@api.route('/generation', methods=['POST'])
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

@api.route('/generation/<int:id>', methods=['GET'])
def getGenerationByID(id):
    generation = Generation.query.get_or_404(id)
    return jsonify({ 'generation': generation.to_dict() })

@api.route('/generation/<int:id>/<attr>', methods=['GET'])
def getGenerationAttrByID(id, attr):
    generation = Generation.query.get_or_404(id)
    try:
        value = getattr(generation, attr)
    except AttributeError:
        abort(404)
    return jsonify({ attr: value })

@api.route('/generation/<int:id>/<attr>', methods=['PUT'])
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
    return jsonify({ attr: data[attr] })
