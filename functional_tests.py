import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

        # Wait 3 seconds to something expected to appear on the screen
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
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

        # User types "Buy peacock feathers" into a text box
        input_box.send_keys('Buy peacock feathers')

        # When user hits enter, the page updates to display
        # "1: Buy peacock feathers" as a item in the to-do list
        input_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathres' for row in rows),
            'New to-do item not in the table'
        )

        # There's still a text box to add another item. User adds
        # "Use peacock to make a fly"
        self.fail('Everything working up to this point')

        # The page  updates again and now shows both items in their
        # list.

        # The site generates a unique URL for her with some explanatory
        # text

        # User visits the URL and sees that their to-do list is still
        # there

        # User quits
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
