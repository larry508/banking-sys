from common.views import CustomerDetails


def find_all():
    return CustomerDetails.query.all()