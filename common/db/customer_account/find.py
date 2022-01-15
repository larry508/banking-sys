from common.views import CustomerAccount


def find_all():
    return CustomerAccount.query.all()