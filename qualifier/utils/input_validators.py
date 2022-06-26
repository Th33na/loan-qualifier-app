# -*- coding: utf-8 -*-
"""Helper functions to validate user input."""

INVALID_SCORE_MESSAGE = "Please enter a value between 0 - 999"
INVALID_AMOUNT_MESSAGE = "Please enter a value between 1 - 200000000"


def is_valid_credit_score(score):
    """Validates if the credit score input provided is a numeric value and between 0 to 999

    Args:
        score: string value.

    Returns:
        Error message if invalid or True when valid.

    """    
    if not score.isdigit():
        return INVALID_SCORE_MESSAGE
    
    numeric_score = int(score)
    if not 0 <= numeric_score <= 999:
         return INVALID_SCORE_MESSAGE
    
    return True

def is_valid_amount(amount):
    """Validates if a monetary input provided can be converted to a float value and between 0 to 200000000

    Args:
        amount: string value.

    Returns:
        Error message if invalid or True when valid.

    """      
    try:
        float_amount = float(amount)
    except ValueError:
        return INVALID_AMOUNT_MESSAGE
    else:
        if not 0 <= float_amount <= 200000000:
            return INVALID_AMOUNT_MESSAGE
        
        return True    
    