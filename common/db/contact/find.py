from common.models import Contact, Customer, User


def find_by_user(user: User):
    customer = Customer.query.filter_by(user_id=user.user_id).first()
    if customer:
        return Contact.query.filter_by(contact_id=customer.contact_id).first()
    