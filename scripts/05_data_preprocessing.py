# 05_data_preprocessing.py
# author: Sarah Gauthier
# date: 2025-12-03

import click
import os
import pandas as pd

# 05_data_preprocessing.py
# author: Sarah Gauthier
# date: 2025-12-03

import click
import os
import pandas as pd

# terminal command to run script:
# python scripts/05_data_preprocessing.py \
#     --train_data_path=data/processed/train_data.csv \
#     --test_data_path=data/processed/test_data.csv

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

@click.command()
@click.option('--train_data_path', type=str, required=True, help="Path to training data CSV")
@click.option('--test_data_path', type=str, required=True, help="Path to testing data CSV")
def main(train_data_path, test_data_path):
    """
    Main function to preprocess training and testing datasets.

    Parameters
    ----------
    train_data_path : str
        Path to the training dataset CSV file.
    test_data_path : str
        Path to the testing dataset CSV file.
    """
    try:
        # Load train and test datasets
        train_df = load_data(train_data_path)
        test_df = load_data(test_data_path)

        # Split into features (X) and target (y)
        X_train, y_train = train_df.drop(columns=["target"]), train_df["target"]
        X_test, y_test = test_df.drop(columns=["target"]), test_df["target"]

        print("Successfully created X and y for training and testing sets")

        # Save the processed data sets
        os.makedirs("data/processed", exist_ok=True)
        X_train.to_csv("data/processed/X_train.csv", index=False)
        y_train.to_csv("data/processed/y_train.csv", index=False)
        X_test.to_csv("data/processed/X_test.csv", index=False)
        y_test.to_csv("data/processed/y_test.csv", index=False)

        print("Successfully uploaded X and y data to data/processed")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()