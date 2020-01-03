# Maybe some help?
# http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html

import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

        # Wait 3 seconds to something expected to appear on the screen
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def _add_todo_item(self, text: str) -> None:
        """Adds item to the todo field and hits Enter."""

        # User finds the text box
        input_box = self.browser.find_element_by_id('id_new_item')

        # User types new todo item and sends the form
        input_box.send_keys(text)
        input_box.send_keys(Keys.ENTER)

    def _wait_todo_item_appear(self, expected_text: str) -> None:
        """Checks if the expected text is in the todo table."""

        # NOTE: We have to wait the page to be refreshed. Instead of
        # a busy wait, one can use the following snippet
        # (from https://stackoverflow.com/questions/45178817
        # selenium-with-python-stale-element-reference-exception):
        WebDriverWait(self.browser, 3).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, 'id_list_table'), expected_text),
            f'Timeout, expected finding todo item: "{expected_text}"'
        )

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            expected_text,
            [row.text for row in rows],
            f'New to-do item not in the table.\nActual text: "{table.text}"'
        )

    
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check if the page is up
        self.browser.get('http://localhost:8000')

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
        self._wait_todo_item_appear('1: Buy peacock feathers')

        # There's still a text box to add another item. User adds
        # "Use peacock to make a fly"
        self._add_todo_item('Use peacock to make a fly')

        # The page updates again and now shows both items in their
        # list.
        self._wait_todo_item_appear('1: Buy peacock feathers')
        self._wait_todo_item_appear('2: Use peacock to make a fly')

        # The site generates a unique URL for her with some explanatory
        # text

        # User visits the URL and sees that their to-do list is still
        # there

        # User quits
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
