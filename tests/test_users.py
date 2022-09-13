from libraries.Users import UsersApi, UserTools, UserAssertions


users_api = UsersApi()


def test_get_users():
    users = users_api.get_users()
    assert len(users) > 0


def test_create_user():
    username = UserTools.generate_name()
    email = UserTools.generate_email()
    users_api.create_user(username, email)
    users = users_api.get_users()
    UserAssertions.verify_user_presence_by_field(users, "name", username)


def test_create_user_with_already_used_name():
    username = UserTools.generate_name()
    email1 = UserTools.generate_email()
    email2 = UserTools.generate_email()
    users_api.create_user(username, email1)
    users_api.create_user(username, email2)
    users = users_api.get_users()
    UserAssertions.verify_user_presence_by_field(users, "email", email1)
    UserAssertions.verify_user_presence_by_field(users, "email", email2)


def test_create_user_with_already_used_email():
    email = UserTools.generate_email()
    username1 = UserTools.generate_name()
    username2 = UserTools.generate_name()
    users_api.create_user(username1, email)
    response = users_api.create_user(username2, email, expected_code=422)
    UserAssertions.verify_email_already_used_error(response)
    users = users_api.get_users()
    UserAssertions.verify_user_presence_by_field(users, "name", username1)
    UserAssertions.verify_user_presence_by_field(users, "name", username2, should_present=False)


def test_update_user_name():
    username = UserTools.generate_name()
    email = UserTools.generate_email()
    user_data = users_api.create_user(username, email, "male", "active")
    user_id = user_data["id"]
    new_name = UserTools.generate_name()
    users_api.update_user(user_id, name=new_name)
    updated_user = users_api.get_user_details(user_id)
    UserAssertions.verify_user_fields_values(updated_user, name=new_name, email=email,
                                             gender="male", status="active")


def test_update_user_email():
    username = UserTools.generate_name()
    email = UserTools.generate_email()
    user_data = users_api.create_user(username, email, "male", "active")
    user_id = user_data["id"]
    new_email = UserTools.generate_email()
    users_api.update_user(user_id, email=new_email)
    updated_user = users_api.get_user_details(user_id)
    UserAssertions.verify_user_fields_values(updated_user, name=username, email=new_email,
                                             gender="male", status="active")

