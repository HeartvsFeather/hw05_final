from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Follow, User


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.author = User.objects.create_user(username='test_author')
        cls.post = Post.objects.create(
            author=cls.author,
            text='test_text',
        )
        cls.user = User.objects.create_user(username='test_user')
        cls.user_two = User.objects.create_user(username='test_user_two')
        cls.follow_index = 'posts:follow_index'

    def setUp(self) -> None:
        self.auth_user_client = Client()
        self.auth_user_client_two = Client()
        self.auth_user_client.force_login(self.user)
        self.auth_user_client_two.force_login(self.user_two)

    def test_follower_see_new_post(self):
        """New entry is accessible for follower and is not accessible for"""
        """not follower"""
        Follow.objects.create(user=self.user, author=self.author)
        response = self.auth_user_client.get(reverse(self.follow_index))
        self.assertEqual(
            response.context['page_obj'].object_list[0], self.post
        )
        response = self.auth_user_client_two.get(reverse(self.follow_index))
        self.assertEqual(response.context['page_obj'].object_list.count(), 0)

    def test_auth_user_can_follow_and_unfollow(self):
        """Auth user can follow and unfollow (new entry in Follow db create,"""
        """when user follow and delete, when unfollow"""
        fol_entry = Follow.objects.create(user=self.user, author=self.author)
        self.assertTrue(
            Follow.objects.filter(author=self.author, user=self.user).exists()
        )
        fol_entry.delete()
        self.assertFalse(
            Follow.objects.filter(author=self.author, user=self.user).exists()
        )
