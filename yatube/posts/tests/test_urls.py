from django.core.cache import cache
from django.test import Client, TestCase

from http import HTTPStatus

from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.author = User.objects.create_user(username='test_name')
        cls.user = User.objects.create_user(username='test_name_two')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text='test_text',
        )
        cls.url_template_db = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/test_name/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        cls.url_status_db_for_not_auth_client = {
            '/': HTTPStatus.OK,
            '/group/test_slug/': HTTPStatus.OK,
            '/profile/test_name/': HTTPStatus.OK,
            '/posts/1/': HTTPStatus.OK,
            '/posts/1/edit/': HTTPStatus.FOUND,
            '/create/': HTTPStatus.FOUND,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        cls.url_status_db_for_auth_author_client = {
            '/': HTTPStatus.OK,
            '/group/test_slug/': HTTPStatus.OK,
            '/profile/test_name/': HTTPStatus.OK,
            '/posts/1/': HTTPStatus.OK,
            '/posts/1/edit/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        cls.url_status_db_for_auth_user_client = {
            '/': HTTPStatus.OK,
            '/group/test_slug/': HTTPStatus.OK,
            '/profile/test_name/': HTTPStatus.OK,
            '/posts/1/': HTTPStatus.OK,
            '/posts/1/edit/': HTTPStatus.FOUND,
            '/create/': HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }

    def setUp(self) -> None:
        self.auth_author_client = Client()
        self.auth_user_client = Client()
        self.not_auth_client = Client()
        self.auth_author_client.force_login(self.author)
        self.auth_user_client.force_login(self.user)

    def test_url_use_correct_template(self):
        """Url use correct template"""
        cache.clear()
        for url, template in self.url_template_db.items():
            with self.subTest(url=url):
                response = self.auth_author_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_not_auth_client_has_acces_to_url(self):
        """Not auth client has correct access to all urls"""
        for url, status in self.url_status_db_for_not_auth_client.items():
            response = self.not_auth_client.get(url)
            self.assertEqual(response.status_code, status)

    def test_auth_author_client_has_acces_to_url(self):
        """Auth author client has correct access to all urls"""
        for url, status in self.url_status_db_for_auth_author_client.items():
            response = self.auth_author_client.get(url)
            self.assertEqual(response.status_code, status)

    def test_auth_user_client_has_acces_to_url(self):
        """Auth not author client has correct access to all urls"""
        for url, status in self.url_status_db_for_auth_user_client.items():
            response = self.auth_user_client.get(url)
            self.assertEqual(response.status_code, status)
