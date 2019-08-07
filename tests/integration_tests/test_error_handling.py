from http import HTTPStatus
import os
import requests

class TestErrorHandling:
    @classmethod
    def setup_class(cls):
        cls.base_url = os.getenv('BASE_URL') or 'http://localhost:5000'

    def test_non_lendingtree_url(self):
        url = 'http://http://quotes.toscrape.com/mortgage/bofa'
        full_request_url = f'{self.base_url}/reviews/bofa'
        resp = requests.get(full_request_url, params={'url': url})
        assert resp.status_code == HTTPStatus.BAD_REQUEST.value

    def test_request_no_url(self):
        full_request_url = f'{self.base_url}/reviews/bofa'
        resp = requests.get(full_request_url)
        assert resp.status_code == HTTPStatus.BAD_REQUEST.value
