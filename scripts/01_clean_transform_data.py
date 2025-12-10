# 01_clean_transform_data.py
# author: Sarah Gauthier
# date: 2025-12-02

import click
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data
from src.transform_data import transform_data

# terminal command to run script: 
# python scripts/01_clean_transform_data.py \
    # --raw_true_data=data/raw/True.csv \
    # --raw_fake_data=data/raw/Fake.csv

@click.command()
@click.option('--raw_true_data', type=str, help="Path to raw true data")
@click.option('--raw_fake_data', type=str, help="Path to raw fake data")
def main(raw_true_data, raw_fake_data):
    """
    Main function to perform data cleaning and transformation.

    - Loads raw true and fake datasets.
    - Transforms and combines them into a single dataset.
    - Saves the processed dataset as a CSV file in the 'data/processed' folder.

    Parameters
    ----------
    raw_true_data : str
        Path to the raw true news CSV file.
    raw_fake_data : str
        Path to the raw fake news CSV file.
    """
    # Load the raw true and fake data from the .csv files
    true_df = load_data(raw_true_data)
    fake_df = load_data(raw_fake_data)
    complete_df = transform_data(true_df, fake_df)

    try:
        # Make sure the folder exists
        os.makedirs("data/processed", exist_ok=True)
        # Upload cleaned dataset as a .csv file to the data/processed folder
        complete_df.to_csv('data/processed/complete_data.csv', index=False)
        print("Successfully uploaded processed data to data/processed")
    except Exception as e:
        print(f"Error uploading processed data: {e}")

if __name__ == '__main__':
    main()
