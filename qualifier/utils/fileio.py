# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
import sys

from qualifier.utils.bank_data_validator import is_valid_bank_data


def load_csv(csvpath):
    """Reads the CSV file from path provided.
    The current assumption is that the csv file is in the correct format:
    

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            if is_valid_bank_data(row):
                data.append(row)
            else:
                print(row)
        print(len(data))
    return data


def save_csv(csvpath, data, header=None):
    """Saves the CSV file from path provided.

    Args:
        csvpath (Path): The CSV file path.
        data (list of lists): A list of the rows of data for the CSV file.
        header (list): An optional header for the CSV.

    """
    try:
        with open(csvpath, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            if header:
                csvwriter.writerow(header)
            csvwriter.writerows(data)
    except FileNotFoundError:
        sys.exit(f"Oops! Can't create the file: {csvpath} because the file directory doesn't exists.")
