from http import HTTPStatus
from django.test import TestCase, Client


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_url_about_author(self):
        """Url /about/author/ acces to anybody"""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            f'Url /about/author/ has incorrect acces, correct status code: '
            f'{HTTPStatus.OK}'
        )

    def test_url_about_tech(self):
        """Url /about/tech/ acces to anybody"""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            f'Url /about/tech/ has incorrect acces, correct status code: '
            f'{HTTPStatus.OK}'
        )
