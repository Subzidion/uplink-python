from flask import jsonify, request, abort

from .. import db
from ..models import PersonnelAccount

from . import api

@api.route('/account/<int:id>', methods=['GET'])
def getAccountByID(id):
    account = PersonnelAccount.query.get_or_404(id)
    return jsonify({ 'account': account.to_dict() })

@api.route('/account/<username>/<attr>', methods=['GET'])
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

@api.route('/account/<username>/<attr>', methods=['PUT'])
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

@api.route('/account/<username>', methods=['GET'])
def getAccountByUsername(username):
    account = PersonnelAccount.query.filter_by(username=username).first()
    if account is None:
        abort(404)
    return jsonify({ 'account': account.to_dict() })


@api.route('/account/<username>/<attr>', methods=['GET'])
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

@api.route('/account/<username>/<attr>', methods=['PUT'])
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
