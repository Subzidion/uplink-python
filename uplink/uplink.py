from flask import Blueprint, request, abort, jsonify, make_response, render_template, session, redirect, url_for
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from . import db, app
from .auth import login_required
from .models import Personnel, PersonnelAccount

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if not 'logged_in' in session:
            return render_template('login.html')
        elif session['logged_in']:
            return render_template('index.html')
    elif request.method == 'POST':
        user = Personnel.query.filter_by(pid=request.form['pid']).first()
        if not user or not user.verify_password(request.form['password']):
            return render_template('login.html', error=True)
        else:
            session['logged_in'] = True
            session['pid'] = request.form['pid']
            session['displayName'] = PersonnelAccount.query.filter_by(pid=request.form['pid']).first().displayName
            return redirect(url_for('main.login'))

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('pid', None)
    session.pop('displayName', None)
    return redirect(url_for('main.login'))

@main.route('/account/password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')
    elif request.method == 'POST':
        user = Personnel.query.filter_by(pid=session['pid']).first()
        if not user.verify_password(request.form['current_password']):
            return render_template('change_password.html', error=True)
        if request.form['new_password'] != request.form['new_password_repeat']:
            return render_template('change_password.html', error=True)
        else:
            user.hash_password(request.form['new_password'])
            db.session.commit()
            return redirect(url_for('main.home'))

@main.route('/password/reset', methods=['GET', 'POST'])
def request_reset_password():
    if request.method == 'GET':
        return render_template('request_reset_password.html')
    elif request.method == 'POST':
        user = Personnel.query.filter_by(pid=request.form['pid']).first()
        if user:
            s = Serializer(app.config['SECRET_KEY'], 600)
            print(s.dumps({'pid': request.form['pid']}))
            return redirect(url_for('main.login'))

@main.route('/password/reset/<reset_token>', methods=['GET', 'POST'])
def reset_password(reset_token):
    if request.method == 'GET':
        return render_template('reset_password.html')
    elif request.method == 'POST':
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(reset_token)
        user = Personnel.query.filter_by(pid=data['pid']).first()
        if request.form['new_password'] != request.form['new_password_repeat']:
            return render_template('reset_password.html', error=True)
        else:
            user.hash_password(request.form['new_password'])
            db.session.commit()
            return redirect(url_for('main.login'))


@main.route('/')
@login_required
def home():
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
