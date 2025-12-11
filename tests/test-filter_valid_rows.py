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

# Test for correctly filtering according to date and text column
def test_correctly_filters():
    pd.testing.assert_frame_equal(filter_valid_rows(nothing_to_remove).reset_index(drop=True),
                                  nothing_to_remove_output.reset_index(drop=True))
    pd.testing.assert_frame_equal(filter_valid_rows(remove_short_text).reset_index(drop=True),
                                  remove_short_text_output.reset_index(drop=True))
    pd.testing.assert_frame_equal(filter_valid_rows(remove_invalid_date).reset_index(drop=True),
                                  remove_invalid_date_output.reset_index(drop=True))

