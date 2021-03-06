# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv, save_csv


from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

from qualifier.utils.input_validators import is_valid_credit_score, is_valid_amount

def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.path("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    # Request for data to calculate
    credit_score = questionary.text("What's your credit score?", validate=is_valid_credit_score).ask()
    debt = questionary.text("What's your current amount of monthly debt?", validate=is_valid_amount).ask()
    income = questionary.text("What's your total monthly income?", validate=is_valid_amount).ask()
    loan_amount = questionary.text("What's your desired loan amount?", validate=is_valid_amount).ask()
    home_value = questionary.text("What's your home value?", validate=is_valid_amount).ask()

    # convert the data to format needed
    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    questionary.print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}", style="bold bg:black fg:green")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    questionary.print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.", style="bold bg:black fg:green")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    questionary.print(f"Found {len(bank_data_filtered)} qualifying loans", style="bold bg:black fg:green")

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """

    # Ask if the qualified loans should be saved into a file
    should_save_loan_to_file = questionary.confirm("Do you want to save the quaifying loans into a file?").ask()

    if should_save_loan_to_file:
        # Ask for the output filename
        csvpath = questionary.path("Enter a file path to save the result (.csv):").ask()
        csv_output_path = Path(csvpath)

        # Check if the file exists and prompt user that their fiel will be overwritten
        if csv_output_path.is_file():
            questionary.print(f"The file {csvpath} exists. It will be overwritten! ", style="bold bg:white fg:red")

        # Save the csv file
        save_csv(csv_output_path, qualifying_loans, header=["Lender","Max Loan Amount","Max LTV","Max DTI","Min Credit Score","Interest Rate"])

        questionary.print(f"As you wish! The Qualified Loans list had been saved in {csvpath}!", style="bold bg:white fg:ansiblue")
    else:
       questionary.print("As you wish! Qualified Loans not saved!", style="bold italic bg:white fg:red")


def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)



if __name__ == "__main__":
    fire.Fire(run)
