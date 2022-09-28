from django import forms
from django.test import Client, TestCase
from django.core.cache import cache
from django.urls import reverse
from posts.models import Group, Post, User


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        cls.post = Post.objects.create(
            text='test_text',
            author=cls.user,
            group=cls.group
        )
        cls.reverse_template_db = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', kwargs={'slug_name': 'test_slug'}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'test_name'}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
            'posts/create_post.html',
        }
        cls.comment_db = {
            'text': 'test_comment_text',
        }
        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    def setUp(self):
        self.client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_use_correct_template(self):
        """Url use correct template"""
        cache.clear()
        for reverse_name, template in self.reverse_template_db.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Index template use correct context"""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text = first_object.text
        post_author = first_object.author
        self.assertEqual(post_text, 'test_text')
        self.assertEqual(post_author, self.user)

    def test_group_list_page_show_correct_context(self):
        """Group template use correct context"""
        response = self.authorized_client.get(reverse(
            'posts:group_posts',
            kwargs={'slug_name': 'test_slug'}))
        first_object = response.context['page_obj'][0]
        post_group = first_object.group
        self.assertEqual(post_group, self.group)

    def test_profile_page_show_correct_context(self):
        """"Profile template use correct context"""
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': 'test_name'}))
        first_object = response.context['page_obj'][0]
        post_author = first_object.author
        self.assertEqual(post_author, self.user)

    def test_post_detail_page_show_correct_context(self):
        """Post detail template use correct context"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': '1'}))
        first_object = response.context['post']
        self.assertEqual(first_object, self.post)

    def test_post_detail_show_comment(self):
        """Post detail show comment"""
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': '1'}),
            data=self.comment_db,
            follow=True
        )
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': '1'}))
        comment = response.context['comments']
        self.assertEqual(comment[0].text, 'test_comment_text')

    def test_edit_post_page_show_correct_context(self):
        """"Post edit template use corrct context"""
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': '1'}))
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        self.assertEqual(response.context['is_edit'], True)

    def test_create_post_page_show_correct_context(self):
        """"Create post template use correct context"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UsePaginator')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        cls.posts = [
            Post.objects.create(
                text='test_text' + str(i),
                author=cls.user,
                group=cls.group) for i in range(13)]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """First index, group, profile page contain 10 entry"""
        cache.clear()
        response_index = self.client.get(reverse('posts:index'))
        response_group = self.client.get(reverse(
            'posts:group_posts',
            kwargs={'slug_name': 'test_slug'}))
        response_profile = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': 'UsePaginator'}))

        self.assertEqual(response_index.context['page_obj'].end_index(), 10)
        self.assertEqual(response_group.context['page_obj'].end_index(), 10)
        self.assertEqual(response_profile.context['page_obj'].end_index(), 10)

    def test_second_page_contains_three_records(self):
        """Second index, group, profile page contain 3 entry"""
        response_index = self.client.get(reverse('posts:index') + '?page=2')
        response_group = self.client.get(reverse(
            'posts:group_posts',
            kwargs={'slug_name': 'test_slug'}) + '?page=2')
        response_profile = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': 'UsePaginator'}) + '?page=2')
        self.assertEqual(len(response_index.context['page_obj']), 3)
        self.assertEqual(len(response_group.context['page_obj']), 3)
        self.assertEqual(len(response_profile.context['page_obj']), 3)


class AddCreatePostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UseGroup')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        cls.group_fectiv = Group.objects.create(
            title='fectiv',
            slug='fectiv',
            description='fectiv'
        )
        cls.post = Post.objects.create(
            text='test_text',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_correct_create_post(self):
        """"Correct create post"""
        cache.clear()
        response_index = self.authorized_client.get(reverse('posts:index'))
        response_group = self.authorized_client.get(reverse(
            'posts:group_posts',
            kwargs={'slug_name': 'test_slug'}))
        response_group_fectiv = self.authorized_client.get(reverse(
            'posts:group_posts',
            kwargs={'slug_name': 'fectiv'}))
        response_profile = self.client.get(reverse(
            'posts:profile',
            kwargs={'username': 'UseGroup'}))
        self.assertEqual(response_index.context['page_obj'][0], self.post)
        self.assertEqual(response_group.context['page_obj'][0], self.post)
        self.assertEqual(len(response_group_fectiv.context['page_obj']), 0)
        self.assertEqual(response_profile.context['page_obj'][0], self.post)
