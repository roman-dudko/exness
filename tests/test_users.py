from libraries.Users import User, Users, UserTools, UserAssertions

import pytest

users = Users()


def test_create_user(user):
    UserAssertions.verify_user_presence_by_field(users.get(), "name", user.name)


def test_create_user_with_already_used_name(user):
    new_user = User(name=user.name)
    UserAssertions.verify_user_presence_by_field(users.get(), "email", new_user.email)


def test_create_user_with_already_used_email(user):
    new_name = UserTools.generate_name()
    with pytest.raises(ValueError) as exception:
        new_user = User(email=user.email, name=new_name, expected_code=422)
    UserAssertions.verify_error(exception, UserAssertions.EMAIL_ALREADY_TAKEN)
    UserAssertions.verify_user_presence_by_field(users.get(), "name", new_name, should_present=False)


@pytest.mark.parametrize("params", [
    {'name': UserTools.generate_name()},
    {'email': UserTools.generate_email()},
    {'gender': 'female'},
    {'status': 'inactive'}
    ], ids=['name', 'email', 'gender', 'status'])
def test_update_user_field(user, params):
    user.update(**params)
    user_details = user.get_details()
    UserAssertions.verify_user_fields_values(user_details, **params)


@pytest.mark.parametrize("params", [
    {'name': ' '},
    {'email': ' '},
    {'gender': ' '},
    {'status': ' '}
    ], ids=['name', 'email', 'gender', 'status'])
def test_clear_user_field(user, params):
    expected_details = user.get_details()
    with pytest.raises(ValueError) as exception:
        user.update(**params, expected_code=422)
    UserAssertions.verify_error(exception, UserAssertions.SHOULD_NOT_BE_EMPTY)
    user_details = user.get_details()
    UserAssertions.verify_user_fields_values(user_details, **expected_details)
