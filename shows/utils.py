import uuid


def generate_confirmation_code():
    return uuid.uuid4().hex
