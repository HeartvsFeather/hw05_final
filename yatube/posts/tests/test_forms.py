from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Comment, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user_one')
        cls.post = Post.objects.create(
            author=cls.user,
            text='test_text_one',
        )
        cls.post_db = {
            'author': cls.user,
            'text': 'test_text_two',
        }
        cls.comment_db = {
            'text': 'test_comment_text',
        }
        cls.post_create = 'posts:post_create'
        cls.post_edit = 'posts:post_edit'
        cls.comment_add = 'posts:add_comment'

    def setUp(self) -> None:
        self.author_client = Client()
        self.not_auth_client = Client()
        self.author_client.force_login(self.user)

    def test_auth_user_create_post(self):
        """Checks that a new db record is created when creating a post"""
        posts_count = Post.objects.count()
        self.author_client.post(
            reverse(self.post_create),
            data=self.post_db,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(pk=2).exists()
        )

    def test_auth_user_edit_post(self):
        """Checks that when editing a post, the db entry changes"""
        self.author_client.post(
            reverse(self.post_edit, kwargs={'post_id': '1'}),
            data=self.post_db,
            follow=True
        )
        self.assertEqual(
            Post.objects.filter(pk=1).get().text, self.post_db['text']
        )

    def test_comment_form_auth(self):
        """If client auth, comment form is avalible and work"""
        self.author_client.post(
            reverse(self.comment_add, kwargs={'post_id': '1'}),
            data=self.comment_db,
            follow=True
        )
        self.assertTrue(
            Comment.objects.filter(text=self.comment_db['text']).exists()
        )

    def test_comment_form_not_auth(self):
        """If client not auth, comment form is anavalible"""
        self.not_auth_client.post(
            reverse(self.comment_add, kwargs={'post_id': '1'}),
            data=self.comment_db,
            follow=True
        )
        self.assertFalse(
            Comment.objects.filter(text=self.comment_db['text']).exists()
        )
