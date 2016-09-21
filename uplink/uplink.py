from flask import Blueprint, request, abort, jsonify, make_response, render_template

from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def getIndex():
    return render_template('index.html')

@main.app_errorhandler(405)
def resourceNotFound(e):
    return make_response(jsonify({'error': 'Method Not Allowed.'}), 405)

@main.app_errorhandler(404)
def resourceNotFound(e):
    return make_response(jsonify({'error': 'Resource Not Found.'}), 404)

@main.app_errorhandler(400)
def resourceNotFound(e):
    return make_response(jsonify({'error': 'Bad Request.'}), 400)
