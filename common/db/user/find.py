from common.models import User


def findByUsername(username: str) -> User:
    return User.query.filter_by(username=username).first()


def findByEmail(email: str) -> User:
    return User.query.filter_by(email=email).first()