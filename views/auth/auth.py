from datetime import date
from hashlib import sha256

from flask import Blueprint, make_response, redirect, render_template, request

from common.db import user as db_user
from common.models import Customer, User
from common.security import verify_user, generate_auth_token, hash_sha256, is_authenticated, login_required
from utils.string_tables import ERRORS
from utils.default_context import get_default_context


blueprint = Blueprint('auth', __name__)



@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        errors = []
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            errors.append(ERRORS['MISSING_FIELDS'])
    
        if not verify_user(username, password):
            errors.append(ERRORS['LOGIN_FAILURE'])

        if errors:
            return render_template('login.html', context=get_default_context(), errors=errors)

        response = make_response(redirect('/'))
        response.set_cookie('auth', generate_auth_token(username, hash_sha256(password)))
        return response

    if request.method == 'GET':
        return render_template('login.html', context=get_default_context())


@blueprint.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect("/auth/login"))
    response.set_cookie("auth", "", expires=0)
    return response


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        errors = []
        form = request.form
        if not form['username'] or not form['email'] or not form['password'] or not form['password-again']:
            errors.append(ERRORS['MISSING_FIELDS'])

        if form['password'] != form['password-again']:
            errors.append(ERRORS['PASSWORD_MISMATCH'])

        if db_user.findByUsername(form['username']):
            errors.append(ERRORS['USERNAME_TAKEN'])

        if db_user.findByEmail(form['email']):
            errors.append(ERRORS['EMAIL_TAKEN'])

        if errors:
            return render_template('register.html', context=get_default_context(), errors=errors)

        user = User(
            user_type='CUSTOMER',
            username=form['username'],
            email=form['email'],
            password_hash=hash_sha256(form['password'])
        )
        db_user.create(user)
        return redirect('/auth/login')

    if request.method == 'GET':
        if is_authenticated():
            return redirect('/')
        return render_template('register.html', context=get_default_context())



@blueprint.route('/register/details', methods=['POST', 'GET'])
def complete_registration():
    if request.method == 'GET':
        return render_template('register_details.html', context=get_default_context())
    
    if request.method == 'POST':
        pass