from ..extensions.bcrypt import bcrypt as bc


def authenticated(session):
    return session.get('user')


def validate_pass(user_pass, candidate_pass):
    foo = bc.check_password_hash(user_pass, candidate_pass)
    return foo
