'''
    This file contains utility functions for the payment service.
'''
from datetime import datetime
import uuid
import re

# Validate credit card number
def validateCreditCardNumber(creditCardNumber):
    # regex to check if the cc number contains only numbers
    if not re.match(r'^\d+$', creditCardNumber):
        return False

    # Check if the card number has a valid length
    if not (13 <= len(creditCardNumber) <= 19):
        return False

    return True

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

