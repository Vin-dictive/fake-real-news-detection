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

true_not_dataframe = {
    "ID": [1, 2],
    "subject": ['politicsNews', 'worldnews']
}
fake_not_dataframe = {
    "ID": [3, 4, 5, 6, 7, 8],
    "subject": ['politics', 'left-news',
                'Government News', 'News',
                'US_News', 'Middle-east']
}

true_no_subject_column = pd.DataFrame({
    "ID": [1, 2],
    "news_type": ['politicsNews', 'worldnews']
})
fake_no_subject_column = pd.DataFrame({
    "ID": [3, 4, 5, 6, 7, 8],
    "news_type": ['politics', 'left-news',
                'Government News', 'News',
                'US_News', 'Middle-east']
})

true_empty = pd.DataFrame({
    "ID": [],
    "subject": []
})
fake_empty = pd.DataFrame({
    "ID": [],
    "subject": []
})

true_unsupported_subject = pd.DataFrame({
    "ID": [1, 2],
    "subject": ['Government News', 'General News']
})
fake_unsupported_subject = pd.DataFrame({
    "ID": [3, 4, 5, 6, 7, 8],
    "subject": ['political-news', 'left-news',
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

# Test for correctly transforming the subject column (normal input, no error)
def test_correctly_transform_subject():
    pd.testing.assert_frame_equal(transform_data(true_normal_replace, fake_normal_replace).reset_index(drop=True),
                                  normal_replace_output.reset_index(drop=True))

# Test for correct error handling
def test_error_handling():
    # when true_df is not a dataframe
    with pytest.raises(TypeError):
        transform_data(true_not_dataframe, fake_normal_replace)
    
    # when fake_df is not a dataframe
    with pytest.raises(TypeError):
        transform_data(true_normal_replace, fake_not_dataframe)

    # when true_df does not have a subject column
    with pytest.raises(ValueError):
        transform_data(true_no_subject_column, fake_normal_replace)
    
    # when fake_df does not have a subject column
    with pytest.raises(ValueError):
        transform_data(true_normal_replace, fake_no_subject_column)
    
    # when output is empty after transformation
    with pytest.raises(ValueError):
        transform_data(true_empty, fake_empty)

    # when true_df has unsupported subject values
    with pytest.raises(ValueError):
        transform_data(true_unsupported_subject, fake_normal_replace)
    
    # when fake_df has unsupported subject values
    with pytest.raises(ValueError):
        transform_data(true_normal_replace, fake_unsupported_subject)

test_error_handling()

# Test for edge cases
def test_edge_cases():
    pass
        