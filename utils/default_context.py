
from common.security import is_authenticated


def get_default_context():
    return {'is_authenticated': is_authenticated()}