import numpy as np
import pandas as pd
import pytest
import sys
import os

# Import the load_data() function from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data

# Set current working directory as the working directory where this test file is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Expected outputs
valid_output = pd.DataFrame({
    'num': [1, 2],
    'letter': ['a', 'b']
})

edge_one_row_output = pd.DataFrame({
    'num': [1],
    'letter': ['a']
})

edge_empty_string_output = pd.DataFrame({
    'num': [0],
    'letter': [np.nan]
})

# Test for correct output type
def test_returns_dataframe():
    output = load_data("../data/test/valid.csv")
    assert isinstance(output, pd.DataFrame)

# Test for reading in a valid csv file
def test_valid_input():
    pd.testing.assert_frame_equal(load_data("../data/test/valid.csv").reset_index(drop=True),
                                  valid_output.reset_index(drop=True))

# Test for correct error handling
def test_error_handling():
    # test file name not ending with ".csv"
    with pytest.raises(ValueError):
        load_data("../data/test/valid.txt")
    
    # test file not found
    with pytest.raises(FileNotFoundError):
        load_data("data/test/valid.csv")
    
    # test csv file is empty
    with pytest.raises(ValueError):
        load_data("../data/test/empty_csv.csv")
    
    # test csv file containing no rows
    with pytest.raises(ValueError):
        load_data("../data/test/output_zero_rows.csv")

# Test for edge cases
def test_edge_cases():
    # edge case 1: csv file only has one row
    pd.testing.assert_frame_equal(load_data("../data/test/one_row.csv").reset_index(drop=True),
                                  edge_one_row_output.reset_index(drop=True))
    
    # edge case 2: csv file has only empty string as value
    pd.testing.assert_frame_equal(load_data("../data/test/empty_string.csv").reset_index(drop=True),
                                  edge_empty_string_output.reset_index(drop=True))