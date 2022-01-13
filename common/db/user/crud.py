

from common.models import User
from common.app import db


def create(user: User):
    db.session.add(user)
    db.session.commit()
    return user