# test_booking_utils.py
import unittest
import booking_utils

class BookingUtilsTestCase(unittest.TestCase):

    def test_generate_qr_code(self):
        booking_details = {
            "seatId": 1,
            "showtimeId": 1,
            "transactionId": 1,
            "userId": "some-user-id",
            "ticketId": 1,
            "ticketPriceId": 1   
        }
        
        qr_code = booking_utils.generateQRCode(booking_details)
        
        self.assertIsNotNone(qr_code)
        self.assertIsInstance(qr_code, bytes)

if __name__ == '__main__':
    unittest.main()
