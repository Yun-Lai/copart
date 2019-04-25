import os
import uuid


def create_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def unique_string(length=10):
    return uuid.uuid4().hex[:length]
