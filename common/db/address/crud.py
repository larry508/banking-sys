from common.models import Address
from common.service import db


def create(address: Address):
    db.session.add(address)
    db.session.commit()