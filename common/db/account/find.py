from common.models import Customer, User


def find_all():
    return Customer.query.all()
