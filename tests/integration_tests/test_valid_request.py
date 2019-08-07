from http import HTTPStatus
import os
import requests

class TestValidRequest:
    @classmethod
    def setup_class(cls):
        cls.base_url = os.getenv('BASE_URL') or 'http://localhost:5000'
        cls.valid_review = {
            "title": "This experience was fantastic and I thank you very much for the needed help!",
            "content": "THE ENTIRE PROCESS WAS EASY AND VERY HAPPY TO WORK WITH THEM. THEY HAVE GIVEN ME A CHANCE TO GET WHAT I NEEDED IN A HURRY!",
            "author": "Debbie",
            "rating": 5,
            "date": "08/2019"
        }
        cls.lengths = {}
    
    def test_non_review_page(self):
        url = 'https://www.lendingtree.com/business/sba/'
        full_request_url = f'{self.base_url}/reviews/sba'
        resp = requests.get(full_request_url, params={'url': url})
        assert resp.status_code == HTTPStatus.OK.value
        assert resp.json() == []

    def test_url_first_page(self):
        url = 'https://www.lendingtree.com/reviews/personal/cashnetusa/81638970'
        full_request_url = f'{self.base_url}/reviews/cashnetusa'
        resp = requests.get(full_request_url, params={'url': url})
        assert resp.status_code == HTTPStatus.OK.value
        assert self.valid_review in resp.json()
        self.lengths['first'] = len(resp.json())

    def test_url_middle_page(self):
        url = 'https://www.lendingtree.com/reviews/personal/cashnetusa/' \
              '81638970?sort=cmV2aWV3c3VibWl0dGVkX2Rlc2M=&pid=10'
        full_request_url = f'{self.base_url}/reviews/cashnetusa'
        resp = requests.get(full_request_url, params={'url': url})
        assert resp.status_code == HTTPStatus.OK.value
        assert self.valid_review in resp.json()
        self.lengths['middle'] = len(resp.json())


    def test_url_last_page(self):
        url = 'https://www.lendingtree.com/reviews/personal/cashnetusa/' \
              '81638970?sort=cmV2aWV3c3VibWl0dGVkX2Rlc2M=&pid=22'
        full_request_url = f'{self.base_url}/reviews/cashnetusa'
        resp = requests.get(full_request_url, params={'url': url})
        assert resp.status_code == HTTPStatus.OK.value
        assert self.valid_review in resp.json()
        self.lengths['last'] = len(resp.json())

    def test_all_request_same_len(self):
        assert self.lengths['first'] == self.lengths['middle'] == self.lengths['last']
