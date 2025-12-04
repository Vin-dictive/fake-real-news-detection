# 07_model_fitting.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
import pickle
from sklearn.dummy import DummyClassifier

# terminal command to run script:
# python scripts/07_model_fitting.py \
#     --train_data_path=data/processed/train_data.csv \
#     --test_data_path=data/processed/test_data.csv

def load_data(path):
    return pd.read_csv(path)

@click.command()
@click.option('--train_data_path', type=str, required=True, help="Path to training data CSV")
@click.option('--test_data_path', type=str, required=True, help="Path to testing data CSV")
def main(train_data_path, test_data_path):
    try:
        # Load train and test datasets
        train_df = load_data(train_data_path)
        test_df = load_data(test_data_path)

        # Split into features (X) and target (y)
        X_train, y_train = train_df.drop(columns=["target"]), train_df["target"]
        X_test, y_test = test_df.drop(columns=["target"]), test_df["target"]

        # dummy classifier model fitting and scoring
        dummy_clf = DummyClassifier(strategy="most_frequent")
        dummy_clf.fit(X_train, y_train)
        test_score_dummy = dummy_clf.score(X_test, y_test)
        print(f"Test accuracy of dummy classifier is {test_score_dummy}")

        # save dummy classfier model
        os.makedirs("models", exist_ok=True)
        dummy_path = "models/dummy_clf.pkl"
        with open(dummy_path, "wb") as f:
            pickle.dump(dummy_clf, f)
        print("Dummy classfier model is saved to the models/ folder")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()