from common.models import Customer


def findAll():
    return Customer.query.all()