# 01_clean_transform_data.py
# author: Sarah Gauthier
# date: 2025-12-02

import click
import os
import pandas as pd

# terminal command to run script: 
# python scripts/01_clean_transform_data.py \
    # --raw_true_data=data/raw/True.csv \
    # --raw_fake_data=data/raw/Fake.csv

def read_data(raw_data):
    """
    Load raw data from a CSV file into a pandas DataFrame.

    Parameters
    ----------
    raw_data : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the loaded raw data.
    """
    # Load the raw data from the .csv files
    data_df = pd.read_csv(raw_data)
    return data_df

def transform_data(true_df, fake_df):
    """
    Clean and transform the raw true and fake news DataFrames.

    - Adds a 'target' column to distinguish True vs. Fake articles.
    - Standardizes the 'subject' column into two categories: 'political' or 'non-political'.
    - Concatenates the two DataFrames into one complete dataset.

    Parameters
    ----------
    true_df : pd.DataFrame
        DataFrame containing true news articles.
    fake_df : pd.DataFrame
        DataFrame containing fake news articles.

    Returns
    -------
    pd.DataFrame
        Combined and transformed DataFrame.
    """    
    # Create new 'target' columns true_df and fake_df
    true_df['target'] = 'True'
    fake_df['target'] = 'Fake'
    
    # Transform 'subject' columns so that they are consistenly in one of two categories: political or non-political
    true_df['subject'] = true_df['subject'].replace('politicsNews', 'political')
    true_df['subject'] = true_df['subject'].replace('worldnews', 'non-political')
    fake_df['subject'] = fake_df['subject'].replace('politics', 'political')
    fake_df['subject'] = fake_df['subject'].replace('left-news', 'political')
    fake_df['subject'] = fake_df['subject'].replace('Government News', 'political')
    fake_df['subject'] = fake_df['subject'].replace('News', 'non-political')
    fake_df['subject'] = fake_df['subject'].replace('US_News', 'non-political')
    fake_df['subject'] = fake_df['subject'].replace('Middle-east', 'non-political')
    
    # Combine true_df and fake_df into a complete dataset
    complete_df = pd.concat([true_df, fake_df])
    
    return complete_df

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
    true_df = read_data(raw_true_data)
    fake_df = read_data(raw_fake_data)
    
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
