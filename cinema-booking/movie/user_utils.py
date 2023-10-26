'''
    This file contains utility functions for the movie service.
'''

import re

def validateRating(input_string):
    # regular expression pattern that matches alphanumeric characters and dashes
    pattern = "^[a-zA-Z0-9-]+$"
    
    # Use re.match() to check if the entire string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False

def validateAlphaWithSpace(input_string):
        # regular expression pattern that matches alphabets and spaces
    pattern = "^[a-zA-Z ]+$"
    
    # Use re.match() to check if the entire string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False
    
def validateInteger(input_string):
    # regular expression pattern that matches integers
    pattern = "^[0-9]+$"
    
    # Use re.match() to check if the entire string matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False
    
def validate_showtime_format(input_string):
    # Define the regular expression pattern
    pattern = "^(0[0-9]|1[0-9]|2[0-3]|[0-9])[:.][0-5][0-9] (AM|PM)$"

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False
    
def validate_showdate_format(input_string):
    # Define the regular expression pattern for "DD-MM-YYYY" format
    pattern = "^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$"

    # Use re.match to check if the input matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False    