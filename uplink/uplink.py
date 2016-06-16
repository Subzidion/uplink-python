from flask import Blueprint, request, abort, jsonify

from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
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

@main.errorhandler(405)
def resourceNotFound(e):
    return jsonify({'error': 'Method Not Allowed.'})

@main.errorhandler(404)
def resourceNotFound(e):
    return jsonify({'error': 'Resource Not Found.'})

@main.errorhandler(400)
def resourceNotFound(e):
    return jsonify({'error': 'Bad Request.'})
