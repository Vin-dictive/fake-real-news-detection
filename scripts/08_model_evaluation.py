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
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data

# terminal command to run script:
# python scripts/08_model_evaluation.py \
#     --test_data_path=data/processed/test_data.csv \
#     --model_path=models/naive_bayes.pkl

def ravel_transform(x):
    """
    Apply ravel transformation to the array x.

    Parameters
    ----------
    x : array
        Input array to be flattened.

    Returns
    -------
    np.ndarray
        1-D flattened array
    """
    return np.ravel(x)

@click.command()
@click.option('--test_data_path', type=str, required=True, help="Path to testing data CSV")
@click.option('--model_path', type=str, required=True, help="Path to saved Naive Bayes fitted model")
def main(test_data_path, model_path):
    """
    Main function to perform model evaluation of the Naive Bayes model.
    - Load the test dataset and the saved Naive Bayes model from the provided path.
    - Produce confusion matrix, classification report, PR curve, ROC curve analysis
    - Save evaluation results as png files in the 'img' folder or txt files in the 'data/text/' folder.

    Parameters
    ----------
    test_data_path : str
        Path to the test dataset CSV file.
    
    model_path : str
        Path to the saved fitted model.    
    """

    try:
        # Load test data
        test_df = load_data(test_data_path)
        X_test, y_test = test_df.drop(columns=["target"]), test_df["target"]

        # Load Naive Bayes model
        with open(model_path, "rb") as f:
            naive_bayes_model = pickle.load(f)
        print("Naive Bayes model is successfully loaded")

        # plot: confusion matrix on test set
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

        # classfication report as a text file
        classfication_report = classification_report(
            y_test, naive_bayes_model.predict(X_test)
        )
        report_path = "data/text/classification_report.txt"
        with open(report_path, "w") as f:
            f.write(classfication_report)
        print("Successfully save classification report as a text file")

        # plot: PR curve
        disp2 = PrecisionRecallDisplay.from_estimator(
            naive_bayes_model,
            X_test,
            y_test,
            pos_label='Fake',
            name='MultinomialNB'
        )
        pr_curve_path = 'img/pr_curve.png'
        disp2.figure_.savefig(pr_curve_path, dpi=300, bbox_inches='tight')
        disp2.figure_.clf()
        print("Successfully save PR curve to the /img folder")

        # plot: ROC curve
        disp3 = RocCurveDisplay.from_estimator(
            naive_bayes_model,
            X_test,
            y_test,
            pos_label='Fake'
        )
        roc_curve_path = 'img/roc_curve.png'
        disp3.figure_.savefig(roc_curve_path, dpi=300, bbox_inches='tight')
        disp3.figure_.clf()
        print("Successfully save ROC curve to the /img folder")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()