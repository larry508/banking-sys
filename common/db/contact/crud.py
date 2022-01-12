

from common.models import Contact
from common.service import db


def create(contact: Contact):
    db.session.add(contact)
    db.session.commit()