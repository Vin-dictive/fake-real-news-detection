import pandas as pd
import pytest
import sys
import os

# Import the load_data() function from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data

# Set current working directory as the working directory where this test file is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Test data


# Expected outputs
valid_output = pd.DataFrame({
    'num': [1, 2],
    'letter': ['a', 'b']
})


# Test for reading in a valid csv file
def test_valid_input():
    pd.testing.assert_frame_equal(load_data("../data/test/valid.csv").reset_index(drop=True),
                                  valid_output.reset_index(drop=True))
    
test_valid_input()


# Test for correctly filtering according to date and text column


# Test for correct error handling


# Test for edge cases

        