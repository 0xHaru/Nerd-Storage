from flask_login import UserMixin

from nerdstorage import config

from .utils.security_util import get_hashed_pw

PASSWORD = get_hashed_pw()


# There is only one user
class User(UserMixin):
    def __init__(self):
        self.id = config.USER_ID
        self.username = config.USERNAME
        self.password = PASSWORD
