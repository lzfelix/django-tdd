from selenium import webdriver
import unittest

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

        self.fail('Everything working up to this point')

        # User is invited to add a item straight away

        # User types "Buy peacock feathers" into a text box

        # When user hits enter, the page updates to display
        # "1: Buy peacock feathers" as a item in the to-do list

        # There's still a text box to add another item. User adds
        # "Use peacock to make a fly"

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
