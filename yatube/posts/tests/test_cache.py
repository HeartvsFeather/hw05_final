from django.test import Client, TestCase
from django.core.cache import cache
from django.urls import reverse

from posts.models import Post, User


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.index_page = 'posts:index'

    def setUp(self) -> None:
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_cache(self):
        temp_post = Post.objects.create(
            author=self.user,
            text='text_text'
        )
        response = self.auth_client.get(reverse(self.index_page)).content
        temp_post.delete()
        self.assertEqual(
            response, self.auth_client.get(reverse(self.index_page)).content
        )
        cache.clear()
        self.assertNotEqual(
            response, self.auth_client.get(reverse(self.index_page)).context
        )
