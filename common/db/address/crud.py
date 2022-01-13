from common.models import Address
from common.app import db


def create(address: Address):
    db.session.add(address)
    db.session.commit()
    return address