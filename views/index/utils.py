

from common.models import Customer, User

def registration_completed(user: User) -> bool:
    customer = Customer.query.filter_by(user_id=user.user_id).first()
    if not customer:
        return False
    if not customer.address_id or not customer.contact_id:
        return False
    return True
