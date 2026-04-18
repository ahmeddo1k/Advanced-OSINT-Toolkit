import unittest
from modules import InputValidator

class TestInputValidation(unittest.TestCase):
    
    def test_valid_email(self):
        self.assertTrue(InputValidator.is_valid_email("test@example.com"))
        self.assertFalse(InputValidator.is_valid_email("invalid-email"))
    
    def test_valid_phone(self):
        self.assertTrue(InputValidator.is_valid_phone("+201234567890"))
        self.assertFalse(InputValidator.is_valid_phone("123"))
    
    def test_valid_domain(self):
        self.assertTrue(InputValidator.is_valid_domain("example.com"))
        self.assertFalse(InputValidator.is_valid_domain("invalid"))
    
    def test_valid_username(self):
        self.assertTrue(InputValidator.is_valid_username("john_doe123"))
        self.assertFalse(InputValidator.is_valid_username("ab"))

if __name__ == "__main__":
    unittest.main()
