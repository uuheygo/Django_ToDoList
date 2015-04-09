from accounts.models import User

def test_email_is_primary_key(self):
    user = User()
    self. assertFalse(hasattr(user, 'id' ))
    
def test_is_authenticated(self):
    user = User()
    self. assertTrue(user. is_authenticated())