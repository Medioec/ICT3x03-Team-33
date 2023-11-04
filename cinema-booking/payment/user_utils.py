'''
    This file contains utility functions for the payment service.
'''
from datetime import datetime,timedelta
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

def validateCreditCardExpiry(creditCardExpiry):
    try:
        # Convert the expiration date string to a datetime object
        expiry_date = datetime.strptime(creditCardExpiry, '%m/%y')

        # Replace day with the last day of the expiry month
        # This considers the card valid through the end of the expiration month
        last_day_of_month = datetime(expiry_date.year, expiry_date.month + 1, 1) - timedelta(days=1)
        expiry_date = expiry_date.replace(day=last_day_of_month.day)

        # Check if the expiration date is in the future
        # Using datetime.utcnow() to get the current UTC date
        return expiry_date >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    except ValueError:
        # Failed to parse the date
        return False
    
# Validate CVV
def validateCvv(cvv):
    # Check if the CVV is a 3 or 4-digit number
    return bool(re.match(r'^\d{3,4}$', cvv))   

# Generates random UUID
def processPayment():
    random_uuid = str(uuid.uuid4())
    return random_uuid

# Returns current datetime
def getTransactionDateTime():
    current_time = datetime.utcnow()
    current_time_iso = current_time.isoformat()
    return current_time_iso

