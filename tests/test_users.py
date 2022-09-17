from libraries.Users import User, Users, UserTools, UserAssertions
import pytest

users = Users()


@pytest.fixture
def user(name=None, email=None, gender="male", status="active"):
    """Returns a new user with random name and email"""
    user = User(name, email, gender, status)
    yield user
    user.delete()


def test_get_users():
    all_users = users.get()
    assert len(all_users) > 0


def test_create_user(user):
    UserAssertions.verify_user_presence_by_field(users.get(), "name", user.name)


def test_create_user_with_already_used_name(user):
    new_user = User(name=user.name)
    UserAssertions.verify_user_presence_by_field(users.get(), "email", new_user.email)


def test_create_user_with_already_used_email(user):
    new_name = UserTools.generate_email()
    with pytest.raises(ValueError) as exception:
        new_user = User(email=user.email, name=new_name, expected_code=422)
    UserAssertions.verify_error(exception, UserAssertions.EMAIL_ALREADY_TAKEN)
    UserAssertions.verify_user_presence_by_field(users.get(), "name", new_name, should_present=False)


# ToDo: parametrize for all fields
def test_update_user_email(user):
    new_email = UserTools.generate_email()
    user.update(email=new_email)
    user_details = user.get_details()
    UserAssertions.verify_user_fields_values(user_details, name=user.name, email=new_email,
                                             gender=user.gender, status=user.status)


# ToDo: parametrize for all fields
def test_clear_user_email(user):
    with pytest.raises(ValueError) as exception:
        user.update(email=" ", expected_code=422)
    UserAssertions.verify_error(exception, UserAssertions.SHOULD_NOT_BE_EMPTY)
    assert "email" in str(exception) and "can't be blank" in str(exception)  # ToDo: looks ugly
    user_details = user.get_details()
    UserAssertions.verify_user_fields_values(user_details, name=user.name, email=user.email,
                                             gender=user.gender, status=user.status)
