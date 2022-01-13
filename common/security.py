import os
from hashlib import sha256
from typing import List

from cryptography.fernet import Fernet
from flask import redirect, request 

from common.db import user as db_user
from common.models import User


def hash_sha256(message: str) -> str:
    return sha256(message.encode('utf-8')).hexdigest()


def generate_auth_token(username: str, password_hash: str) -> str:
    key = os.environ.get('AUTH_SECRET_KEY').encode()
    fernet = Fernet(key)
    message = str(username) + ':' + str(password_hash)
    return fernet.encrypt(message.encode())


def decode_token(token: str) -> str:
    key = os.environ.get('AUTH_SECRET_KEY').encode()
    fernet = Fernet(key)
    return fernet.decrypt(token.encode()).decode()


def get_user_from_token(token: str) -> List[str]:
    decoded = decode_token(token)
    return decoded.split(':')


def verify_user(username: str, password: str) -> bool:
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    return user.password_hash.lower() == hashed_password.lower()


def verify_user_by_password_hash(username: str, password_hash: str) -> bool:
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    return user.password_hash.lower() == password_hash.lower()

def get_current_user() -> User:
    auth_token = request.cookies.get('auth')
    if not auth_token:
        return False
    username, password_hash = get_user_from_token(auth_token)
    return db_user.find_by_username(username)

def is_authenticated() -> bool:
    auth_token = request.cookies.get('auth')
    if not auth_token:
        return False
    username, password_hash = get_user_from_token(auth_token)
    return verify_user_by_password_hash(username, password_hash)


def is_admin(user) -> bool:
    return user.user_type == 'ADMIN'


#################################
# ACCESS RESTRICTION DECORATORS #
#################################

def login_required(f):
    def inner(*args, **kwargs):
        if not is_authenticated():
            return redirect('/auth/login')
        return f(*args, **kwargs)
    inner.__name__ = f.__name__
    return inner

def admin_view(f):
    def inner(*args, **kwargs):
        if not is_authenticated():
            return redirect('/auth/login')
        user = get_current_user()
        if not is_admin(user):
            return redirect('/')
        return f(*args, **kwargs)
    return inner
        
        