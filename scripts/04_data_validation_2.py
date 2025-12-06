# 04_data_validation_2.py
# author: Sarah Gauthier
# date: 2025-12-03

import click
import os
import pandas as pd
import pandera.pandas as pa

# terminal command to run script: 
# python scripts/04_data_validation_2.py \
#   --train_data_path=data/processed/train_data.csv
    
def load_data(path):
    """
    Load a dataset from a CSV file.

    Parameters
    ----------
    path : str
        Path to the CSV file containing the dataset.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the loaded dataset.
    """
    return pd.read_csv(path)

def filter_valid_rows(train_data):
    """
    Filter out invalid rows from the training dataset.

    Parameters
    ----------
    train_data : pd.DataFrame
        The training dataset.

    Returns
    -------
    pd.DataFrame
        Filtered dataset containing only valid rows.
    """
    train_data = train_data[train_data['text'].str.len() >= 20]
    train_data = train_data[pd.to_datetime(train_data['date'], 
                                   format='mixed', 
                                   errors='coerce').notna()]
    return train_data

def build_schema2():
    """
    Build a Pandera schema for validating training data content.

    Checks performed:
    - No outlier or anomalous values
    - Correct category levels (i.e., no string mismatches or single values)

    Returns
    -------
    pa.DataFrameSchema
        Pandera schema object for validating training data.
    """ 
    schema2 = pa.DataFrameSchema(
        {
            "title": pa.Column(
                str,
                pa.Check((lambda x: x.str.len().between(5, 1000)), 
                        error="Outlier title length detected")
            ),
            "text": pa.Column(
                str,
                pa.Check((lambda x: x.str.len().between(20, 80000)), 
                        error="Outlier text length detected")
            ),
            "subject": pa.Column(
                str,
                pa.Check((lambda x: x.isin(['political', 'non-political'])),
                        error="Incorrect subject category levels")
            ),
            "date": pa.Column(
                str,
                pa.Check((lambda x: pd.to_datetime(x,
                                                format='mixed',
                                                errors='coerce').between(pd.Timestamp('1980-01-01'),
                                                            pd.Timestamp.now())), 
                        error="Outlier news date detected")
            ),
            "target": pa.Column(
                str,
                pa.Check((lambda x: x.isin(['True', 'Fake'])),
                        error="Incorrect target category levels")
            )
        }
    )
    return schema2
    
def expected_target_distribution(df):
    """
    Check that the target variable follows the expected distribution.

    Ensures that neither class ('True' or 'Fake') exceeds 80% of the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Training dataset.

    Returns
    -------
    bool
        True if distribution is valid, False otherwise.
    """
    return (df['target'].value_counts(normalize=True) < 0.8).all()

def normal_corr_target_features(df):
    """
    Check for anomalous correlations between target and features.

    Parameters
    ----------
    df : pd.DataFrame
        Training dataset.

    Returns
    -------
    bool
        True if correlations are within acceptable range, False otherwise.
    """
    target = df['target'].map({
        "True": 1,
        "Fake": 0
    })
    title_length = df['title'].str.len()
    text_length = df['text'].str.len()
    numeric_subject = df['subject'].map({
        "political": 1,
        "non-political": 0
    })
    # Since date will be dropped later, no need to check its correlation

    for casted_feaure in [title_length, text_length, numeric_subject]:
        correlation = target.corr(casted_feaure)
        if correlation > 0.8:
            return False

    return True

def normal_corr_between_features(df):
    """
    Check for anomalous correlations between explanatory features.

    Parameters
    ----------
    df : pd.DataFrame
        Training dataset.

    Returns
    -------
    bool
        True if correlations are within acceptable range, False otherwise.
    """
    title_length = df['title'].str.len()
    text_length = df['text'].str.len()
    numeric_subject = df['subject'].map({
        "political": 1,
        "non-political": 0
    })
    # Since date will be dropped later, no need to check its correlation

    corr1 = title_length.corr(text_length)
    corr2 = title_length.corr(numeric_subject)
    corr3 = text_length.corr(numeric_subject)
    for corr in [corr1, corr2, corr3]:
        if corr > 0.8:
            return False

    return True

def build_schema3():
    """
    Build a Pandera schema for validating dataset-level properties.

    Checks performed:
    - Target variable follows expected distribution.
    - No anomalous correlations between target/response variable and features/explanatory variables.
    - No anomalous correlations between features/explanatory variables.

    Returns
    -------
    pa.DataFrameSchema
        Pandera schema object for validating dataset-level properties.
    """
    schema3 = pa.DataFrameSchema(
        checks=[
            pa.Check(expected_target_distribution,
                     error="Target does not follow expected distribution"),
            pa.Check(normal_corr_target_features,
                     error="Anomalous correlations between target and features"),
            pa.Check(normal_corr_between_features,
                     error="Anomalous correlations between features")
        ]
    )
    return schema3


def validate_data(train_data, schema):
    """
    Validate the training dataset against the provided schema.

    Parameters
    ----------
    train_data : pd.DataFrame
        The dataset to validate.
    schema : pa.DataFrameSchema
        Pandera schema used for validation.

    Raises
    ------
    pa.errors.SchemaErrors
        If the dataset fails validation checks.
    """
    schema.validate(train_data, lazy=True)

@click.command()
@click.option('--train_data_path', type=str, help="Path to training data")

def main(train_data_path):
    """
    Main function to validate and save the training dataset.

    Parameters
    ----------
    train_data_path : str
        Path to the training dataset CSV file.

    Raises
    ------
    FileNotFoundError
        If the specified training dataset file does not exist.
    pa.errors.SchemaErrors
        If the dataset fails validation checks.
    Exception
        For any other unexpected errors during validation or saving.
    """
    try:
        train_data = load_data(train_data_path)
        schema2 = build_schema2()
        train_data = filter_valid_rows(train_data)
        validate_data(train_data, schema2)
        schema3 = build_schema3()
        validate_data(train_data, schema3)
        
        print("Succesfully validated data")
    except FileNotFoundError:
        print(f"File not found: {train_data_path}")
    except pa.errors.SchemaErrors as err:
        print("Data validation failed:")
        print(err.failure_cases)
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        # Make sure the folder exists
        os.makedirs("data/processed", exist_ok=True)
        # Upload split datasets as a .csv files to the data/processed folder
        train_data.to_csv('data/processed/train_data.csv', index=False)
        print(f"Successfully uploaded training data to data/processed")
    except Exception as e:
        print(f"Error uploading processed data: {e}")

if __name__ == '__main__':
    main()