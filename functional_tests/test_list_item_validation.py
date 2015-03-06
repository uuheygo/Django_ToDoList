from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_item(self):
        # Enter an empty item by accident
        
        # Home page refreshes, and an error message saying the list item cannot be empty
        
        # Enter a non-empty item and it works
        
        # Enter an empty item again, another error message shows update
        
        # Fix it by filling some text in
        self.fail('write me!')