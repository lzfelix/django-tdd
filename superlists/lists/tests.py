import re

from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

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
        list_ = List.objects.create()

        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='wrong item 1', list=other_list)
        Item.objects.create(text='wrong item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'wrong item 1')
        self.assertNotContains(response, 'wrong item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


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

        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

class NewItemText(TestCase):
    def test_can_save_a_POST_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        todo_text = 'A new item for an existing list'
        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': todo_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, todo_text)
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListAndItemModelTest(TestCase):
    def test_saving_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item, the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, first_item.text)
        self.assertEqual(saved_items[0].list, list_)

        self.assertEqual(saved_items[1].text, second_item.text)
        self.assertEqual(saved_items[1].list, list_)
