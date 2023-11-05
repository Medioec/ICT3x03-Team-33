# test_user_utils.py

import unittest
from uuid import UUID
from datetime import datetime
from user_utils import (
    validateCreditCardNumber,
    validateCreditCardName,
    validateCreditCardExpiry,
    validateCvv,
    processPayment,
    getTransactionDateTime
)

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
        self.assertIsInstance(UUID(payment_id), UUID)

    def test_get_transaction_date_time(self):
        transaction_date_time = getTransactionDateTime()
        self.assertIsInstance(datetime.fromisoformat(transaction_date_time), datetime)


if __name__ == '__main__':
    unittest.main()
