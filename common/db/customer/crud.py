from common.models import Customer
from common.app import db


def create(customer: Customer):
    db.session.add(customer)
    db.session.commit()
    return customer

def delete(customer: Customer):
    customer.delete()
    db.session.commit()

def delete_by_id(customer_id: str):
    Customer.query.filter_by(customer_id=customer_id).delete()
    db.session.commit()