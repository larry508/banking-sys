

from common.models import User
from common.service import db


def create(user: User):
    db.session.add(user)
    db.session.commit()