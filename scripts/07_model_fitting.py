# 07_model_fitting.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
import numpy as np
import pickle
import threading
import time
import sys
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.load_data import load_data

# terminal command to run script:
# python scripts/07_model_fitting.py \
#     --train_data_path=data/processed/train_data.csv \
#     --test_data_path=data/processed/test_data.csv

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

def progress_indicator(stop_event):
    """
    Display a message in console while model fitting until it stops

    Parameters
    ----------
    stop_event : threading.Event
        An event that indicates when the model fitting stops.
    """
    chars = "|/-\\"
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rFitting model... {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

@click.command()
@click.option('--train_data_path', type=str, required=True, help="Path to training data CSV")
@click.option('--test_data_path', type=str, required=True, help="Path to testing data CSV")
def main(train_data_path, test_data_path):
    """
    Main function to perform model fitting.
    - Load the train and test dataset from the provided path.
    - Fit two classification ML models: dummy classifier and Naive Bayes model.
    - Save the fitted models to the "models/" folder.

    Parameters
    ----------
    train_data_path : str
        Path to the train dataset CSV file.

    test_data_path : str
        Path to the test dataset CSV file.
    """

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

        # Naive Bayes classifier model

        # make column-specific preprocessing pipelines for the column 'title' and 'text'
        title_feature = 'title'
        text_feature = 'text'
        categorical_feature = ['subject']
        drop_feature = ['date']
        title_pipe = make_pipeline(
            FunctionTransformer(ravel_transform), 
            CountVectorizer()
        )
        text_pipe = make_pipeline(
            FunctionTransformer(ravel_transform), 
            CountVectorizer()
        )

        # make overall preprocessor for all columns using ColumnTransformer
        preprocessor = ColumnTransformer(
            [
                ("one_hot", OneHotEncoder(drop="if_binary"), categorical_feature),
                ("title_vectorizer", title_pipe, "title"),
                ("text_vectorizer", text_pipe, "text"),
                ("drop", "drop", drop_feature)
            ]
        )

        # make Naive Bayes model's ML pipeline
        pipe = make_pipeline(preprocessor, MultinomialNB())

        # make hyperparameter distribution to search from
        param_dist = {
            "columntransformer__title_vectorizer__countvectorizer__max_features": randint(1, 200),
            "columntransformer__text_vectorizer__countvectorizer__max_features": randint(1, 5000),
            "multinomialnb__alpha": 10.0 ** np.arange(-7, 1)
        }

        # define randomized search object using cross validation
        random_search = RandomizedSearchCV(pipe, 
                                           param_distributions=param_dist, 
                                           n_iter=10, n_jobs=-1,
                                           return_train_score=True,
                                           random_state=123)
        
        # print out a pending message in console to show model is still fitting
        stop_event = threading.Event()
        progress_thread = threading.Thread(target=progress_indicator, args=(stop_event,))
        progress_thread.start()
        
        # fit Naive Bayes model to the training set
        random_search.fit(X_train, y_train)
        
        # print out a completed message in console when model fitting is done
        stop_event.set()
        progress_thread.join()
        print("\rModel fitting completed!" + " " * 20) 

        # save Naive Bayes model
        NB_path = "models/naive_bayes.pkl"
        with open(NB_path, "wb") as f:
            pickle.dump(random_search, f)
        
        # print Naive Bayes parameters and scores
        print("Best hyperparameters of Naive Bayes model: ", random_search.best_params_)
        print("Training score of Naive Bayes model: ", random_search.score(X_train, y_train))
        print("Best CV score of Naive Bayes model: ", random_search.best_score_)
        print("Test score of Naive Bayes model: ", random_search.score(X_test, y_test))

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()