from libraries.Users import User

import pytest


@pytest.fixture
def user(name=None, email=None, gender="male", status="active"):
    """Creates new user for test and removes in teardown"""
    user = User(name, email, gender, status)
    yield user
    user.delete()
