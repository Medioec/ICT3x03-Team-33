import unittest
from user_utils import validateRating, validateAlphaWithSpace, validateInteger, validate_showtime_format, validate_showdate_format, validate_theaterId_format

class UserUtilsTest(unittest.TestCase):

    def test_validate_rating(self):
        self.assertTrue(validateRating("PG-13"))
        self.assertFalse(validateRating("R!@#"))

    def test_validate_alpha_with_space(self):
        self.assertTrue(validateAlphaWithSpace("The Lion King"))
        self.assertFalse(validateAlphaWithSpace("ToyStory123"))

    def test_validate_integer(self):
        self.assertTrue(validateInteger("1234"))
        self.assertFalse(validateInteger("12ab"))

    def test_validate_showtime_format(self):
        self.assertTrue(validate_showtime_format("12:30 PM"))
        self.assertFalse(validate_showtime_format("12:30PM"))

    def test_validate_showdate_format(self):
        self.assertTrue(validate_showdate_format("12-03-2023"))
        self.assertFalse(validate_showdate_format("03/12/2023"))

    def test_validate_theaterId_format(self):
        self.assertTrue(validate_theaterId_format("1A"))
        self.assertFalse(validate_theaterId_format("A1"))

if __name__ == '__main__':
    unittest.main()
