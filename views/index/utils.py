

from common.models import Address, Contact, Customer, User

def registration_completed(user: User) -> bool:
    customer: Customer = Customer.query.filter_by(user_id=user.user_id).first()
    if not customer:
        return False
    address = Address.query.filter_by(address_id=customer.address_id).first()
    contact = Contact.query.filter_by(contact_id=customer.contact_id).first()
    if not address or not contact:
        return False
    return True
