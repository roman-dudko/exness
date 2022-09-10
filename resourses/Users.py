from Base import ApiBase
from urllib.parse import urljoin


class Users(ApiBase):
    USERS_PATH = '/users/'

    def __init__(self, site_url):
        super().__init__(site_url)

    def get_users(self):
        users_url = urljoin(self.endpoint, self.USERS_PATH)
        response = self.session_request('GET', users_url)
        return response.json()

    def get_user_details(self, user_id):
        users_url = urljoin(self.endpoint, self.USERS_PATH)
        user_url = urljoin(users_url, user_id)
        response = self.session_request('GET', user_url)
        return response.json()

    def create_users(self, name, email, gender):
        users_url = urljoin(self.endpoint, self.USERS_PATH)
        payload = {
            'name': name,
            'email': email,
            'gender': gender
        }
        response = self.session_request('POST', users_url, payload=payload)
        return response.json()

    def update_users(self, name, email, status):
        users_url = urljoin(self.endpoint, self.USERS_PATH)
        payload = {
            'name': name,
            'email': email,
            'status': status
        }
        response = self.session_request('PATCH', users_url, payload=payload)
        return response.json()

    def delete_user(self, user_id):
        users_url = urljoin(self.endpoint, self.USERS_PATH)
        user_url = urljoin(users_url, user_id)
        response = self.session_request('DELETE', user_url)
        return response.json()