from libraries.ApiBase import ApiBase
from urllib.parse import urljoin

import random
import string


class UsersApi(ApiBase):
    USERS_PATH = 'public/v2/users/'

    def __init__(self):
        users_url = urljoin(self.ENDPOINT, self.USERS_PATH)
        super().__init__(users_url)

    def get_users(self):
        response = self.session_request('GET', self.api_url)
        return response.json()

    def get_user_details(self, user_id):
        user_url = urljoin(self.api_url, str(user_id))
        response = self.session_request('GET', user_url)
        return response.json()

    def create_user(self, name, email, gender="male", status="active", expected_code=201):
        payload = {
            'name': name,
            'email': email,
            'gender': gender,
            'status': status
        }
        response = self.session_request('POST', self.api_url, payload=payload, expected_code=expected_code)
        return response.json()

    def update_user(self, user_id, name=None, email=None, gender=None, status=None):
        payload = {}
        user_url = urljoin(self.api_url, str(user_id))
        if name is not None:
            payload.update({'name': name})
        if email is not None:
            payload.update({'email': email})
        if gender is not None:
            payload.update({'gender': gender})
        if status is not None:
            payload.update({'status': status})

        response = self.session_request('PATCH', user_url, payload=payload)
        return response.json()

    def delete_user(self, user_id):
        user_url = urljoin(self.api_url, user_id)
        self.session_request('DELETE', user_url)


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
    @classmethod
    def verify_email_already_used_error(cls, response):
        assert response[0]["field"] == "email" and response[0]["message"] == "has already been taken", \
            f"Incorrect error message: {response}, expected: field=email, message=has already been taken"

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
