from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class ViewTestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nonexist_page = reverse(
            'posts:profile', kwargs={'username': 'nonexist_name'}
        )

    def setUp(self):
        self.client = Client()

    def test_error_page_404(self):
        """Nonexist page work correct"""
        template = 'core/404.html'
        response = self.client.get(self.nonexist_page)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, template)
