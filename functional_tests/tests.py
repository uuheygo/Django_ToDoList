from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Go to the home page
        self.browser.get(self.live_server_url)
        
        # Title and header have 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # Find the input box for a to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        
        # Enter a to-do item
        inputbox.send_keys('Buy peacock feathers')
        
        # Page updates to add the to-do item
        inputbox.send_keys(Keys.ENTER)
        my_list_url = self.browser.current_url
        self.assertRegexpMatches(my_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        
        # Another box asking for another to-do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peakcock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again and shows two items
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peakcock feathers to make a fly')
        
        ## Start a new browser session. Making sure none the previous information 
        # Another user comes and start a new session
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Check if any of previous session items is shown
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peakcock feathers to make a fly', page_text)
        
        # Start a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        
        # Compare the new list url with the previous one and make sure they are different
        new_list_url = self.browser.current_url
        self.assertRegexpMatches(new_list_url, '/lists/.+')
        self.assertNotEqual(new_list_url, my_list_url)
        
        # Make sure only items of the new list are shown
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
        self.fail('Finished the test!')
        
    def test_layout_and_styling(self):
        # Go to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # Input box should be centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5)
            
        # Starts a new list and the input should centered
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5)

