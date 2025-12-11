import pandas as pd
import pytest
import sys
import os

# Import the filter_valid_rows() function from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.transform_data import transform_data

# Test data
true_normal_replace = pd.DataFrame({
    "ID": [1, 2],
    "subject": ['politicsNews', 'worldnews']
})
fake_normal_replace = pd.DataFrame({
    "ID": [3, 4, 5, 6, 7, 8],
    "subject": ['politics', 'left-news',
                'Government News', 'News',
                'US_News', 'Middle-east']
})

# Expected outputs
normal_replace_output = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5, 6, 7, 8],
    "subject": ['political', 'non-political', 'political', 'political',
                'political', 'non-political', 'non-political', 'non-political'],
    'target': ['True', 'True', 'Fake', 'Fake',
               'Fake', 'Fake', 'Fake', 'Fake']
})

# Test for correct output type
def test_returns_dataframe():
    output = transform_data(true_normal_replace, fake_normal_replace)
    assert isinstance(output, pd.DataFrame)

test_returns_dataframe()

# Test for correctly transforming the subject column (normal input, no error)
def test_correctly_transform_subject():
    pd.testing.assert_frame_equal(transform_data(true_normal_replace, fake_normal_replace).reset_index(drop=True),
                                  normal_replace_output.reset_index(drop=True))
    
test_correctly_transform_subject()

# Test for correct error handling
def test_error_handling():
    pass

# Test for edge cases
def test_edge_cases():
    pass
        