from common.models import Account
from common.app import db


def create(account: Account):
    db.session.add(account)
    db.session.commit()
    return account

def delete(account: Account):
    account.delete()
    db.session.commit()

def delete_by_id(account_id: str):
    Account.query.filter_by(account_id=account_id).delete()
    db.session.commit()