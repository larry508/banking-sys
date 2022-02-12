from common.models import Account


def find_all():
    return Account.query.all()
