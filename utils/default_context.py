
from common.security import get_current_user, is_admin, is_authenticated


def get_default_context():
    return {'is_authenticated': is_authenticated(),
            'is_admin': is_admin(get_current_user())
            }