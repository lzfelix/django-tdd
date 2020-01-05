# Maybe some help?
# http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html

import time
import unittest
import contextlib

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support import expected_conditions


# Use Django's server for testing, thus ensuring DB cleaning ip
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    @contextlib.contextmanager
    def wait_for_page_load(self, timeout=3):
        """This avoids Selenium 3.x complaining about stale elements after a
        page refresh. See https://bit.ly/39I2uMH"""
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )
    
    def _add_todo_item(self, text: str) -> None:
        """Adds item to the todo field and hits Enter."""

        # User finds the text box
        input_box = self.browser.find_element_by_id('id_new_item')

        # User types new todo item and sends the form
        input_box.send_keys(text)
        input_box.send_keys(Keys.ENTER)

    def _check_todo_item(self, item: str) -> None:
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            item,
            [row.text for row in rows],
            f'New to-do item not in the table.\nActual text: "{table.text}"'
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check if the page is up
        self.browser.get(self.live_server_url)

        # Ensure that the page title mentions a ToDo list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to add a item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "Buy peacock feathers" into a text box and hits enter
        self._add_todo_item('Buy peacock feathers')

        # When user hits enter, the page updates to display
        # "1: Buy peacock feathers" as a item in the to-do list
        with self.wait_for_page_load():
            self._check_todo_item('1: Buy peacock feathers')

        # Also, the user is taken to a new URL
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, r'/lists/.+')

        # There's still a text box to add another item. User adds
        # "Use peacock to make a fly"
        self._add_todo_item('Use peacock to make a fly')

        # The page updates again and now shows both items in their
        # list.
        with self.wait_for_page_load():
            self._check_todo_item('1: Buy peacock feathers')
            self._check_todo_item('2: Use peacock to make a fly')

        # Now, a new user, Francis, comes along to the site.

        ## <- meta comment
        ## Using a new browser session to ensure that no information
        ## from the first user is coming through cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item.
        self._add_todo_item('Buy milk')
        with self.wait_for_page_load():
            self._check_todo_item('1: Buy milk')

        # Francis gets his unique URL.
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, r'/lists/.+')
        self.assertNotEqual(francis_url, edith_url)

        # There should be no trace of Edith's list, just Francis' list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satified, they both go back to sleep.
        self.browser.quit()

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box centralized
        inputbux = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbux.location['x'] + inputbux.size['width'] / 2,
            512, 
            delta=5
        )

        # She starts a new list and sees the input is nicely cenetered there too
        self._add_todo_item('testing')

        self.wait_for_page_load()
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbux.location['x'] + inputbux.size['width'] / 2,
            512, 
            delta=5
        )
