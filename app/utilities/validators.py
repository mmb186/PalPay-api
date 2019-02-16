import re


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def is_valid_user_info(data):
    # TODO: validate email, two passwords are the same,  first and lastname and login info is unique
    # return True and is_valid_email(data.email)
    return True
