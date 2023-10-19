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