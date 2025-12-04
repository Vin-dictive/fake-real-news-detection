# 08_model_evaluation.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import(
    GridSearchCV,
    RandomizedSearchCV,
    cross_validate
)
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from scipy.stats import expon, lognorm, loguniform, randint, uniform, norm, randint
from sklearn.metrics import ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay, classification_report

# terminal command to run script:
# python scripts/08_model_evaluation.py \
#     --test_data_path=data/processed/test_data.csv
#     --model_path=models/naive_bayes.pkl

def load_data(path):
    return pd.read_csv(path)

def ravel_transform(x):
    return np.ravel(x)

@click.command()
@click.option('--test_data_path', type=str, required=True, help="Path to testing data CSV")
@click.option('--model_path', type=str, required=True, help="Path to saved Naive Bayes fitted model")
def main(test_data_path, model_path):
    try:
        # Load test data
        test_df = load_data(test_data_path)
        X_test, y_test = test_df.drop(columns=["target"]), test_df["target"]

        # Load Naive Bayes model
        with open(model_path, "rb") as f:
            naive_bayes_model = pickle.load(f)
        print("Naive Bayes model is successfully loaded")

        # confusion matrix on test set
        disp = ConfusionMatrixDisplay.from_estimator(
            naive_bayes_model,
            X_test,
            y_test,
            values_format="d"
        )
        confusion_matrix_path = 'img/confusion_matrix.png'
        disp.figure_.savefig(confusion_matrix_path, dpi=300, bbox_inches='tight')
        disp.figure_.clf()
        print("Successfully save confusion matrix to the /img folder")
        

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()