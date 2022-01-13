from common.models import Address, Customer, User


def find_by_user(user: User):
    customer = Customer.query.filter_by(user_id=user.user_id).first()
    if customer:
        return Address.query.filter_by(address_id=customer.address_id).first()
    