from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_item(self):
        # Enter an empty item by accident
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        
        # Home page refreshes, and an error message saying the list item cannot be empty
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.test, "You can't have an empty list item")
        
        # Enter a non-empty item and it works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        # Enter an empty item again, another error message shows update
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.test, "You can't have an empty list item")
        
        # Fix it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')