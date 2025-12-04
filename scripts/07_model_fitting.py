# 07_model_fitting.py
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

# terminal command to run script:
# python scripts/07_model_fitting.py \
#     --train_data_path=data/processed/train_data.csv \
#     --test_data_path=data/processed/test_data.csv

def load_data(path):
    return pd.read_csv(path)

def ravel_transform(x):
    return np.ravel(x)

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

        # Naive Bayes classifier model
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
        preprocessor = ColumnTransformer(
            [
                ("one_hot", OneHotEncoder(drop="if_binary"), categorical_feature),
                ("title_vectorizer", title_pipe, "title"),
                ("text_vectorizer", text_pipe, "text"),
                ("drop", "drop", drop_feature)
            ]
        )
        pipe = make_pipeline(preprocessor, MultinomialNB())
        param_dist = {
            "columntransformer__title_vectorizer__countvectorizer__max_features": randint(1, 200),
            "columntransformer__text_vectorizer__countvectorizer__max_features": randint(1, 5000),
            "multinomialnb__alpha": 10.0 ** np.arange(-7, 1)
        }
        random_search = RandomizedSearchCV(pipe, 
                                           param_distributions=param_dist, 
                                           n_iter=10, n_jobs=-1,
                                           return_train_score=True,
                                           random_state=123)
        random_search.fit(X_train, y_train) 

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