from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    def test_cannot_add_empty_list_item(self):
        # Enter an empty item by accident
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        
        # Home page refreshes, and an error message saying the list item cannot be empty
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # Enter a non-empty item and it works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        # Enter an empty item again, another error message shows update
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # Fix it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        
    def test_cannot_add_duplicate_items(self):
        # Go to the home page and start a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        
        # Try to enter a duplicate Item
        self.get_item_input_box().send_keys('Buy wellies\n')
        
        # See a helpful error Message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")
        
    def test_error_messages_are_cleared_on_input(self):
        # start a new list in a way that causes a validation ERROR
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        
        # start typing in the input box to clear the ERROR
        self.get_item_input_box().send_keys('a')
        # error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())