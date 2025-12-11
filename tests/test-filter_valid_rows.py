import pandas as pd
import pytest
import sys
import os

# Import the filter_valid_rows() function from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.filter_valid_rows import filter_valid_rows

# Test data
nothing_to_remove = pd.DataFrame({
    "text": ['x' * 30, 'y' * 40],
    'date': ['2021-01-01', '2000-12-31']
})

remove_short_text = pd.DataFrame({
    "text": ['x' * 10, 'y' * 40],
    'date': ['2021-01-01', '2000-12-31']
})

remove_invalid_date = pd.DataFrame({
    "text": ['x' * 30, 'y' * 40],
    'date': ['2021-01-01', 'string']
})

missing_text_column = pd.DataFrame({
    'date': ['2021-01-01', '2000-12-31']
})

missing_date_column = pd.DataFrame({
    "text": ['x' * 30, 'y' * 40]
})

input_not_dataframe = {
    "text": ['x' * 30, 'y' * 40],
    'date': ['2021-01-01', '2000-12-31']
}

no_rows_remaining = pd.DataFrame({
    "text": ['x' * 5, 'y' * 6],
    'date': ['2021-15-40', 'excuse-me']
})

# Expected outputs
nothing_to_remove_output = pd.DataFrame({
    "text": ['x' * 30, 'y' * 40],
    'date': ['2021-01-01', '2000-12-31']
})

remove_short_text_output = pd.DataFrame({
    "text": ['y' * 40],
    'date': ['2000-12-31']
})

remove_invalid_date_output = pd.DataFrame({
    "text": ['x' * 30],
    'date': ['2021-01-01']
})

# Test for correctly returning a dataframe as output
def test_returns_dataframe():
    output = filter_valid_rows(nothing_to_remove)
    assert isinstance(output, pd.DataFrame)

test_returns_dataframe()