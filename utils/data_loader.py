"""
This file contains utility functions for loading data from CSV files.
"""
import csv


def load_csv(file_path):
    """Load test-data from a CSV file."""
    data = []
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Test-Data file not found: {file_path}")
