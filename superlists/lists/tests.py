import re

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

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

    @staticmethod
    def remove_csrf_tag(text: str) -> str:
        """Remove csrf tag from text. See https://groups.google.com/forum/#!topic/obey-the-testing-goat-book/fwY7ifEWKMU"""
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/first-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/first-list/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class NewListTest(TestCase):
    def test_saving_POST_request(self):
        self.client.post('/lists/new', data={
            'item_text': 'A new list item'
        })

        # Check if the todo item was saved in the DB
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={
            'item_text': 'A new list item'
        })
        self.assertRedirects(response, '/lists/first-list/')


class ItemModelTest(TestCase):
    def test_saving_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item, the second'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[1].text, second_item.text)