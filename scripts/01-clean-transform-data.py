# 01-clean-transform-data.py
# author: Sarah Gauthier
# date: 2025-12-02

import click
import os
import numpy as np
import pandas as pd

# terminal command to run script: 
# python scripts/clean-transform-data.py \
    # --raw-true-data=data/raw/True.csv \
    # --raw-fake-data=data/raw/Fake.csv

@click.command()
@click.option('--raw-true-data', type=str, help="Path to raw true training data")
@click.option('--raw-fake-data', type=str, help="Path to raw fake training data")


def main(raw_true_data, raw_fake_data):
    
    # Load the raw true and fake data from the .csv files
    true_df = pd.read_csv(raw_true_data)
    fake_df = pd.read_csv(raw_fake_data)
    
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
    
    # Shuffle the complete dataframe
    complete_df = complete_df.sample(frac=1).reset_index(drop=True)
    
    # Make sure the folder exists
    os.makedirs("data/processed", exist_ok=True)
    
    # Upload cleaned dataset as a .csv file to the data/processed folder
    complete_df.to_csv('data/processed/complete-data.csv')

if __name__ == '__main__':
    main()