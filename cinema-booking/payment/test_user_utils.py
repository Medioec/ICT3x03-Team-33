# test_user_utils.py

import unittest
from uuid import UUID
from user_utils import (
    validateCreditCardNumber,
    validateCreditCardName,
    validateCreditCardExpiry,
    validateCvv,
    processPayment,
    getTransactionDateTime
)
from datetime import datetime

class TestUserUtils(unittest.TestCase):

    def test_validate_credit_card_number(self):
        self.assertTrue(validateCreditCardNumber("1234567812345678"))
        self.assertFalse(validateCreditCardNumber("123"))
        self.assertFalse(validateCreditCardNumber(""))

    def test_validate_credit_card_name(self):
        self.assertTrue(validateCreditCardName("John Doe"))
        self.assertFalse(validateCreditCardName("12345"))
        self.assertFalse(validateCreditCardName(""))

    def test_validate_cvv(self):
        self.assertTrue(validateCvv("123"))
        self.assertTrue(validateCvv("1234"))
        self.assertFalse(validateCvv("12"))
        self.assertFalse(validateCvv("abcd"))

    def test_process_payment(self):
        payment_id = processPayment()
        # Check if the payment_id is a valid UUID string
        try:
            uuid_obj = UUID(payment_id, version=4)
        except ValueError:
            self.fail(f"{payment_id} is not a valid UUID")

    def test_get_transaction_date_time(self):
        transaction_date_time = getTransactionDateTime()
        # This regex matches the ISO format
        iso_format_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(.\d+)?(Z|[+-]\d{2}:\d{2})?$'
        self.assertRegex(transaction_date_time, iso_format_regex)

if __name__ == '__main__':
    unittest.main()
