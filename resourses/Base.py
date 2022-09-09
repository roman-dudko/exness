import logging
import requests
from urllib.parse import urlparse


class ApiBase:
    def __init__(self, backend_url):
        self.logger = logging.getLogger()
        self.backend_url = backend_url
        self.session = requests.Session()
        self.session.headers['Content-Type'] = 'application/json;charset=utf-8'
        self.session.headers['Referer'] = urlparse(backend_url).netloc

    def get_session_headers(self):
        return self.session.headers

    def get_attribute_from_session_header(self, attribute):
        assert attribute in self.session.headers, \
            f'No {attribute} found in response'
        return self.session.headers[attribute]

    def add_session_headers(self, **kwargs):
        return self.session.headers

    def update_session_headers(self, headers):
        self.session.headers.update(headers)

    def remove_session_header(self, header_name):
        self.session.headers.pop(header_name)

    def remove_session_headers(self, headers_list):
        for header_name in headers_list:
            self.session.headers.pop(header_name)

    def session_request(self, method, url, payload=None, params=None,
                        headers=None, expected_code=200, **kwargs):

        response = self.session.request(method, url, headers=headers,
                                        json=payload, params=params, **kwargs)

        all_headers = self.session.headers
        if headers:
            all_headers.update(dict(headers))

        self.logger.info(f'URL: {method} {url}')
        self.logger.info(f'REQUEST PAYLOAD: {payload}')
        self.logger.info(f'REQUEST PARAMS: {params}')
        self.logger.info(f'REQUEST HEADERS: {all_headers}')
        self.logger.info(f'RESPONSE STATUS CODE: {response.status_code}')
        self.logger.info(f'RESPONSE HEADERS: {response.headers}')
        self.logger.info(f'RESPONSE: {response.text}')

        assert (response.status_code, int(expected_code),
                'Unexpected response status code')
        return response

    # ToDo: add method for key/value verification

    # ToDo: verify only keys, 'response formatt'
    # @staticmethod
    # def verify_json_content(json_object, attributes):
    #     for attr in attributes:
    #         if not (attr in json_object):
    #             asserts.assert_false(True,
    #                                  msg=f'Response does not contain {attr} attribute')