import unittest
from logic import is_valid_title, is_valid_rating

class TestLogic(unittest.TestCase):

    def test_is_valid_title(self):
        self.assertTrue(is_valid_title("Spider-Man"))
        self.assertTrue(is_valid_title("  Batman  "))
        self.assertFalse(is_valid_title(""))
        self.assertFalse(is_valid_title("   "))
        self.assertFalse(is_valid_title(None))

    def test_is_valid_rating(self):
        self.assertTrue(is_valid_rating(1))
        self.assertTrue(is_valid_rating(5))
        self.assertTrue(is_valid_rating("3"))
        self.assertFalse(is_valid_rating(0))
        self.assertFalse(is_valid_rating(6))
        self.assertFalse(is_valid_rating("abc"))
        self.assertFalse(is_valid_rating(None))

if __name__ == '__main__':
    unittest.main()