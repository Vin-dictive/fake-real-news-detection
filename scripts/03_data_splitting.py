# 03_data_splitting.py
# author: Sarah Gauthier
# date: 2025-12-03

import click
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data

# terminal command to run script: 
# python scripts/03_data_splitting.py \
    # --data_path=data/processed/complete_data.csv

def data_splitting(complete_data):
    """
    Split the complete dataset into training (80%) and testing (20%) sets.

    Parameters
    ----------
    complete_data : pd.DataFrame
        The full dataset to be split.

    Returns
    -------
    tuple of (pd.DataFrame, pd.DataFrame)
        - train_df: DataFrame containing the training data.
        - test_df: DataFrame containing the testing data.
    """
    # Split into train/test data sets
    train_df, test_df = train_test_split(
        complete_data, train_size=0.80, random_state=123
    )
    return train_df, test_df

@click.command()
@click.option('--data_path', type=str, help="Path to data to split")

def main(data_path):
    """
    Main function to perform dataset splitting.
    - Load the complete dataset from the provided path.
    - Split the dataset into training (80%) and testing (20%) sets.
    - Save the resulting datasets as CSV files in the 'data/processed' folder.

    Parameters
    ----------
    data_path : str
        Path to the complete dataset CSV file.
    """
    # load data and split into train/test data sets
    try:
        complete_data = load_data(data_path)
        train_df, test_df = data_splitting(complete_data)
        print("Succesfully split data in training and testing sets")
    except FileNotFoundError:
        print(f"File not found: {data_path}")
        
    try:
        # Make sure the folder exists
        os.makedirs("data/processed", exist_ok=True)
        # Upload split datasets as a .csv files to the data/processed folder
        train_df.to_csv('data/processed/train_data.csv', index=False)
        test_df.to_csv('data/processed/test_data.csv', index=False)
        print(f"Successfully uploaded training and testing data to data/processed")
    except Exception as e:
        print(f"Error uploading processed data: {e}")

if __name__ == '__main__':
    main()
    