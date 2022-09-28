import shutil
import tempfile
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.core.cache import cache
from django.urls import reverse
from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='test_title',
            slug='test_slug',
            description='test_description'
        )
        cls.test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='test.gif',
            content=cls.test_gif,
            content_type='image/gif'
        )
        cls.uploaded_two = SimpleUploadedFile(
            name='test_two.gif',
            content=cls.test_gif,
            content_type='image/gif'
        )
        cls.post_db = {
            'text': 'test_text',
            'image': cls.uploaded,
        }
        cls.reverse_db = [
            reverse('posts:index'),
            reverse('posts:profile', kwargs={'username': 'test_user'}),
            reverse('posts:group_posts', kwargs={'slug_name': 'test_slug'}),
        ]
        cls.post_create = 'posts:post_create'
        cls.img_way = 'posts/test.gif'
        cls.img_way_two = 'posts/test_two.gif'

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_post_with_img(self):
        """Create post with correct image"""
        self.client.post(
            reverse(self.post_create),
            data=self.post_db,
            follow=True
        )
        self.assertTrue(Post.objects.filter(image=self.img_way).exists())

    def test_page_show_correct_context_img(self):
        """All pages contain context with correct image"""
        cache.clear()
        Post.objects.create(
            author=self.user,
            text='test_text_two',
            group=self.group,
            image=self.uploaded_two
        )
        for rev in self.reverse_db:
            self.assertEqual(
                self.client.get(rev).context['page_obj'][0].image,
                self.img_way_two
            )
        rev = reverse('posts:post_detail', kwargs={'post_id': '1'})
        self.assertEqual(
            self.client.get(rev).context['post'].image,
            self.img_way_two
        )
