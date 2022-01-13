from common.models import Customer, User


def find_all():
    return Customer.query.all()


def find_by_user(user: User):
    return Customer.query.filter_by(user_id=user.user_id).first()