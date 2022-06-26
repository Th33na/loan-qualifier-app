"""Helper functions to validate bank data input."""
from qualifier.utils.input_validators import is_valid_credit_score, is_valid_amount

def is_valid_bank_data(data_row):
    """Validates if a row/record provided is in the format needed by the application
        [Lender (string),Max Loan Amount(float),Max LTV(float),Max DTI(float),Min Credit Score(int),Interest Rate(float)]
    Args:
        data_row (list): bank details

    Returns:
        Boolean to indicate whether row is valid or not

    """
    # TODO: Convert to dictionary instead of list

    if not len(data_row) == 6:
        return False

    for index in [1,2,3,5]:
        if not is_valid_amount(data_row[index]) == True:
            return False
    
    if not is_valid_credit_score(data_row[4]) == True:
        return False
    
    return True

