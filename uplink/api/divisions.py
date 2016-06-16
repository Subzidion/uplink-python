from flask import jsonify, request, abort

from .. import db
from ..models import Division
from . import api

@api.route('/division', methods=['GET'])
def getDivisions():
    divisions = Division.query.all()
    return jsonify({ 'divisions': [ division.to_dict() for division in divisions ] })

@api.route('/division', methods=['POST'])
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

@api.route('/division/<int:id>', methods=['GET'])
def getDivisionByID(id):
    division = Division.query.get_or_404(id)
    return jsonify({ 'division': division.to_dict() })

@api.route('/division/<int:id>/<attr>', methods=['PUT'])
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
    return jsonify({ attr: data[attr] })

@api.route('/division/<int:id>/<attr>', methods=['GET'])
def getDivisionAttrByID(id, attr):
    division = Division.query.get_or_404(id)
    try:
        value = getattr(division, attr)
    except AttributeError:
        abort(404)
    return jsonify({ attr: value })
