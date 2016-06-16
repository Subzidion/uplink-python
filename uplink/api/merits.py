from flask import jsonify, request, abort

from .. import db
from ..models import Merit

from . import api

@api.route('/merit', methods=['GET'])
def getMerits():
    merits = Merit.query.all()
    return jsonify({ 'merit': [ merit.to_dict() for merit in merits ] })

@api.route('/merit', methods=['POST'])
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

@api.route('/merit/<int:id>', methods=['GET'])
def getMeritByID(id):
    merit = Merit.query.get_or_404(id)
    return jsonify({ 'merit': merit.to_dict() })

@api.route('/merit/<int:id>/<attr>', methods=['PUT'])
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
    return jsonify({ attr: data[attr] })

@api.route('/merit/<int:id>/<attr>', methods=['GET'])
def getMeritAttrByID(id, attr):
    merit = Merit.query.get_or_404(id)
    try:
        value = getattr(merit, attr)
    except AttributeError:
        abort(404)
    return jsonify({ attr: value })
