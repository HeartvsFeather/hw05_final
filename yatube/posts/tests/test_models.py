from django.test import TestCase

from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test_text_one_hello_world',
        )
        cls.verbose_name = 'Текст поста'
        cls.help_text = 'Введите текст поста'

    def test_model_have_correct_object_names(self):
        """Check correct __str__ for models"""
        self.assertEqual(self.group.__str__(), self.group.title)
        self.assertEqual(self.post.__str__(), self.post.text[:15])
        self.assertEqual(len(self.post.__str__()), 15)

    def test_post_model_have_correct_verb_name__help_text(self):
        """Check correct verb name and help text in post model text field"""
        self.assertEqual(
            self.post._meta.get_field('text').verbose_name,
            self.verbose_name
        )
        self.assertEqual(
            self.post._meta.get_field('text').help_text,
            self.help_text
        )
