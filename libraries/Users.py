from libraries.ApiBase import ApiBase
from urllib.parse import urljoin

import random
import string

USERS_PATH = 'public/v2/users/'


class Users(ApiBase):
    def __init__(self):
        self.users_url = urljoin(self.ENDPOINT, USERS_PATH)
        super().__init__(self.users_url)

    def get(self, expected_code=200):
        return self.session_request('GET', self.users_url, expected_code=expected_code).json()


class User(ApiBase):
    def __init__(self, name=None, email=None, gender="male", status="active", expected_code=201):
        self.users_url = urljoin(self.ENDPOINT, USERS_PATH)
        super().__init__(self.users_url)

        name = name if name is not None else UserTools.generate_name()
        email = email if email is not None else UserTools.generate_email()
        payload = {
            'name': name,
            'email': email,
            'gender': gender,
            'status': status
        }
        response = self.session_request('POST', self.users_url, payload=payload, expected_code=expected_code).json()
        if expected_code != 201:
            raise ValueError(response)
        self.name = response["name"]
        self.email = response["email"]
        self.gender = response["gender"]
        self.status = response["status"]
        self.id = response["id"]
        self.user_url = urljoin(self.users_url, str(self.id))

    def get_details(self, expected_code=200):
        return self.session_request('GET', self.user_url, expected_code=expected_code).json()

    def delete(self, expected_code=204):
        self.session_request('DELETE', self.user_url, expected_code=expected_code)

    def update(self, **fields):
        expected_code = 200 if "expected_code" not in fields.keys() else fields["expected_code"]
        payload = {}

        for field in fields:
            payload.update({field: fields[field]})  # ToDo: dict comprehension

        response = self.session_request('PATCH', self.user_url, payload=payload, expected_code=expected_code).json()
        if expected_code != 200:
            raise ValueError(response)
        self.name = response["name"]
        self.email = response["email"]
        self.gender = response["gender"]
        self.status = response["status"]
        return response


class UserTools:
    @classmethod
    def generate_email(cls):
        email_prefix = ''.join(random.choices(string.ascii_lowercase, k=10))
        return f"{email_prefix}@testmail.com"

    @classmethod
    def generate_name(cls):
        first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        last_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        return f"{first_name} {last_name}"


class UserAssertions:
    SHOULD_NOT_BE_EMPTY = "can't be blank"
    EMAIL_ALREADY_TAKEN = "already been taken"

    @classmethod
    def verify_error(cls, exception, error):
        assert error in str(exception.value), f"Incorrect error message: {exception}, expected: {error}"

    @classmethod
    def verify_user_presence_by_field(cls, users, field, value, should_present=True):
        if should_present:
            assert any(user[field] == value for user in users), \
                "Created user was not found in response"
        else:
            assert not any(user[field] == value for user in users), \
                "User was found in response, but should not be there"

    @classmethod
    def verify_user_fields_values(cls, user_data, **fields):
        for field in fields:
            if field in user_data.keys():
                assert fields[field] == user_data[field], f"Incorrect value of the {fields}: {fields[field]} " \
                                                          f"!= {user_data[field]}"
            else:
                raise KeyError(f"Expected key '{fields[field]}' is not present in user data: {user_data}")
