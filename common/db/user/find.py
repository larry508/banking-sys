from common.models import User


def find_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()


def find_by_user(email: str) -> User:
    return User.query.filter_by(email=email).first()