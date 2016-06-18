from flask import jsonify, request, abort

from .. import db
from ..models import Personnel, PersonnelAccount

from . import api

@api.route('/personnel/<int:id>', methods=['GET'])
def getPersonnelByID(id):
    personnel = Personnel.query.get_or_404(id)
    return jsonify({ 'personnel': personnel.to_dict() })

@api.route('/personnel/<int:id>/<attr>', methods=['GET'])
def getPersonnelAttrByID(id, attr):
    personnel = Personnel.query.get_or_404(id)
    try:
        value = getattr(personnel, attr)
    except AttributeError:
        abort(404)
    if(type(value) == list):
        return jsonify({ attr: [ item.to_dict() for item in value ] })
    try:
        return jsonify({ attr: value.to_dict() })
    except AttributeError:
        return jsonify({ attr: value })

@api.route('/personnel/<int:id>/<attr>', methods=['PUT'])
def putPersonnelAttrByID(id, attr):
    if not hasattr(Personnel, attr):
        abort(404)
    if not request.json or attr == 'pid' or attr not in request.json:
        abort(400)
    data = request.json
    personnel = Personnel.query.get_or_404(id)
    try:
        setattr(personnel, attr, data[attr])
    except KeyError:
        abort(400)
    db.session.commit()
    return jsonify({ attr: data[attr] })

@api.route('/personnel/<username>', methods=['GET'])
def getPersonnelByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    return jsonify({ 'personnel': personnel.to_dict() })

@api.route('/personnel/<username>/<attr>', methods=['GET'])
def getPersonnelAttrByUsername(username, attr):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    personnel = Personnel.query.get_or_404(account.pid)
    try:
        value = getattr(personnel, attr)
    except AttributeError:
        abort(404)
    if(type(value) == list):
        return jsonify({ attr: [ item.to_dict() for item in value ] })
    try:
        return jsonify({ attr: value.to_dict() })
    except AttributeError:
        return jsonify({ attr: value })

@api.route('/personnel/<username>/<attr>', methods=['PUT'])
def putPersonnelAttrByUsername(username, attr):
    if not hasattr(Personnel, attr):
        abort(404)
    if not request.json or attr == 'pid' or attr not in request.json:
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
