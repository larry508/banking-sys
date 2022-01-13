

from common.models import Contact
from common.app import db


def create(contact: Contact):
    db.session.add(contact)
    db.session.commit()