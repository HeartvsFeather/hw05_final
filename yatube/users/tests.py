from django.test import Client, TestCase

from http import HTTPStatus

from posts.models import User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.url_status_db_for_not_auth_client = {
            '/auth/signup/': HTTPStatus.OK,
            '/auth/logout/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
            '/auth/password_change/': HTTPStatus.FOUND,
            '/auth/password_change/done/': HTTPStatus.FOUND,
            '/auth/password_reset/': HTTPStatus.OK,
            '/auth/password_reset/done/': HTTPStatus.OK,
            '/auth/reset/<uidb64>/<token>/': HTTPStatus.OK,
            '/auth/reset/done/': HTTPStatus.OK,
        }
        cls.url_status_db_for_auth_client = {
            '/auth/signup/': HTTPStatus.OK,
            '/auth/logout/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
            '/auth/password_change/': HTTPStatus.FOUND,
            '/auth/password_change/done/': HTTPStatus.FOUND,
            '/auth/password_reset/': HTTPStatus.OK,
            '/auth/password_reset/done/': HTTPStatus.OK,
            '/auth/reset/<uidb64>/<token>/': HTTPStatus.OK,
            '/auth/reset/done/': HTTPStatus.OK,
        }

    def setUp(self) -> None:
        self.not_auth_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_not_auth_client_has_acces_to_url(self):
        """Not auth client has correct access to all urls"""
        for url, status in self.url_status_db_for_not_auth_client.items():
            response = self.not_auth_client.get(url)
            self.assertEqual(
                response.status_code,
                status,
                f'Not auth client has statuse code: {response.status_code} to '
                f'url: {url}, wich is incorrect. Correcr: {status}'
            )

    def test_auth_client_has_acces_to_url(self):
        """Auth client has correct access to all urls"""
        for url, status in self.url_status_db_for_auth_client.items():
            response = self.auth_client.get(url)
            self.assertEqual(
                response.status_code,
                status,
                f'Auth client has statuse code: {response.status_code} to url:'
                f' {url}, wich is incorrect. Correct: {status}'
            )
