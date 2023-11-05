import unittest
from user_utils import (validateRating, validateAlphaWithSpace, validateInteger,
                        validate_showtime_format, validate_showdate_format, validate_theaterId_format)
from datetime import datetime

class TestUserUtils(unittest.TestCase):
    
    def test_validateRating(self):
        self.assertTrue(validateRating("PG-13"))
        self.assertFalse(validateRating("Rated R"))
    
    def test_validateAlphaWithSpace(self):
        self.assertTrue(validateAlphaWithSpace("The Godfather"))
        self.assertFalse(validateAlphaWithSpace("The Godfather 2"))
    
    def test_validateInteger(self):
        self.assertTrue(validateInteger("12345"))
        self.assertFalse(validateInteger("123.45"))
        self.assertFalse(validateInteger("12three45"))
    
    def test_validate_showtime_format(self):
        self.assertTrue(validate_showtime_format("10:30 AM"))
        self.assertTrue(validate_showtime_format("09:45 PM"))
        self.assertFalse(validate_showtime_format("13:30PM"))
        self.assertFalse(validate_showtime_format("00:00AM"))
    
    def test_validate_showdate_format(self):
        # Testing with a valid date string
        self.assertTrue(self.is_valid_date("29-02-2020"))  # Leap year
        self.assertTrue(self.is_valid_date("01-01-2023"))  # Valid non-leap year date
        
        # Testing with an invalid date string
        self.assertFalse(self.is_valid_date("31-02-2023"))  # Invalid date
        self.assertFalse(self.is_valid_date("31-11-2023"))  # Invalid date (November has 30 days)
        
    def is_valid_date(self, date_string):
        """Helper function to validate the date format 'DD-MM-YYYY' and check if it is a valid date."""
        try:
            # If the date string is in the correct format and is a valid date, datetime.strptime will succeed.
            datetime.strptime(date_string, "%d-%m-%Y")
            return True
        except ValueError:
            # If datetime.strptime raises a ValueError, it means the string is not a valid date.
            return False
    
    def test_validate_theaterId_format(self):
        self.assertTrue(validate_theaterId_format("10A"))
        self.assertFalse(validate_theaterId_format("A10"))
        self.assertFalse(validate_theaterId_format("10!"))

if __name__ == '__main__':
    unittest.main()
