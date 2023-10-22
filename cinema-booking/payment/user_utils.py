'''
    This file contains utility functions for the payment service.
'''
from datetime import datetime
import uuid
import re

# Validate credit card number
def validateCreditCardNumber(creditCardNumber):
    # Check if the card number has a valid length
    if len(creditCardNumber) != 16:
        return False

    # Perform Luhn algorithm (Modulus 10 check)
    digits = [int(digit) for digit in creditCardNumber]
    checksum = 0
    for i in range(len(digits) - 2, -1, -2):
        double_digit = digits[i] * 2
        if double_digit > 9:
            double_digit -= 9
        digits[i] = double_digit
    checksum = sum(digits) % 10
    return checksum == 0

# Validate credit card name
def validateCreditCardName(creditCardName):
    # Allow only letters and spaces, and ensure it's not empty
    return bool(re.match(r'^[A-Za-z\s]+$', creditCardName)) and len(creditCardName) > 0

# Validate credit card expiry date
def validateCreditCardExpiry(creditCardExpiry):
    try:
        # Convert the expiration date string to a datetime object
        expiry_date = datetime.strptime(creditCardExpiry, '%m/%y')
        # Check if the expiration date is in the future
        return expiry_date > datetime.now()
    except ValueError:
        return False  # Failed to parse the date
    
# Validate CVV
def validateCvv(cvv):
    # Check if the CVV is a 3 or 4-digit number
    return bool(re.match(r'^\d{3,4}$', cvv))   

# Generates random UUID
def processPayment():
    random_uuid = uuid.uuid4()
    return random_uuid

# Returns current datetime
def getTransactionDateTime():
    return datetime.now()

