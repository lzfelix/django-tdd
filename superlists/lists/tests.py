import re

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')

        self.assertEqual(
            self.remove_csrf_tag(response.content.decode()),
            self.remove_csrf_tag(expected_html)
        )

    def test_home_page_can_save_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'}
        )

        # self.assertIn('A new list item', response.content.decode())

        self.assertEqual(
            self.remove_csrf_tag(response.content.decode()),
            self.remove_csrf_tag(expected_html)
        )

    @staticmethod
    def remove_csrf_tag(text: str) -> str:
        """Remove csrf tag from text. See https://groups.google.com/forum/#!topic/obey-the-testing-goat-book/fwY7ifEWKMU"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)