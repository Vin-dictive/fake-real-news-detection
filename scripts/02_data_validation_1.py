# 02_data_validation_1.py
# author: Sarah Gauthier
# date: 2025-12-03

import click
import os
import pandas as pd
import pandera.pandas as pa

# terminal command to run script: 
# python scripts/02_data_validation_1.py \
    # --processed_data_path=data/processed/complete_data.csv
    
def load_data(path):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the loaded data.
    """
    return pd.read_csv(path)

def build_schema():
    """
    Build a Pandera schema for validating the processed dataset.

    The schema checks for:
    - Correct column names
    - No empty observations
    - Missingness not beyond expected threshold
    - Correct data types in each column
    - No duplicate observations

    Returns
    -------
    pa.DataFrameSchema
        Pandera schema object for validating the dataset.
    """
    schema = pa.DataFrameSchema(
        {
            "title": pa.Column(str),
            "text": pa.Column(str),
            "subject": pa.Column(str,
                                pa.Check(lambda s: s.isna().mean() <= 0.05,
                                        element_wise=False,
                                        error = "Too many null values in 'subject' column")),
            "date": pa.Column(str, nullable=True),
        },
        checks = [
            pa.Check(lambda df: ~df.duplicated().any(), error = "Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error = "Empty rows found.")
        ],
        drop_invalid_rows=True
    )
    return schema

def validate_data(processed_data, schema):
    """
    Validate the processed dataset against the provided schema.

    Parameters
    ----------
    processed_data : pd.DataFrame
        The dataset to validate.
    schema : pa.DataFrameSchema
        The Pandera schema used for validation.

    Raises
    ------
    pa.errors.SchemaErrors
        If the dataset fails validation checks.
    """
    schema.validate(processed_data, lazy=True)

@click.command()
@click.option('--processed_data_path', type=str, help="Path to processed data")

def main(processed_data_path):
    """
    Main function to perform data validation and save the cleaned dataset.
    - Load the processed dataset from the given path.
    - Drop duplicate rows.
    - Build and apply the validation schema.
    - Save the validated dataset back to 'data/processed/complete_data.csv'.

    Parameters
    ----------
    processed_data_path : str
        Path to the processed dataset CSV file.
    """
    try:
        processed_data = load_data(processed_data_path)
        processed_data = processed_data.drop_duplicates()
        schema = build_schema()
        validate_data(processed_data, schema)
        print("Succesfully validated data")
    except FileNotFoundError:
        print(f"File not found: {processed_data_path}")
    except pa.errors.SchemaErrors as err:
        print("Data validation failed:")
        print(err.failure_cases)
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    try:
        # Make sure the folder exists
        os.makedirs("data/processed", exist_ok=True)
        # Upload cleaned dataset as a .csv file to the data/processed folder
        processed_data.to_csv('data/processed/complete_data.csv', index=False)
        print(f"Successfully uploaded processed data to data/processed")
    except Exception as e:
        print(f"Error uploading processed data: {e}")

if __name__ == '__main__':
    main()