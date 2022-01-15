from common.models import Customer
from common.app import db


def create(customer: Customer):
    db.session.add(customer)
    db.session.commit()
    return customer


def update_address_id(customer: Customer, address_id):
    customer.address_id = address_id
    db.session.commit()


def update_contact_id(customer: Customer, contact_id):
    customer.contact_id = contact_id
    db.session.commit()


def delete(customer: Customer):
    customer.delete()
    db.session.commit()

def delete_by_id(customer_id: str):
    Customer.query.filter_by(customer_id=customer_id).delete()
    db.session.commit()