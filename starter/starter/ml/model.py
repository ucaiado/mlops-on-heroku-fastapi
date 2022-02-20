'''
Implement functions to train a model on Cencus data

Author: ucaiado
Date: February 13th, 2022
'''

import pandas as pd
import numpy as np
from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier


# Optional: implement hyperparameter tuning.
def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Inputs
    ------
    X_train : np.array
        Training data.
    y_train : np.array
        Labels.

    Returns
    -------
    model
        Trained machine learning model.
    """

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    return clf


def compute_model_metrics(y, preds):
    """
    Validates the trained machine learning model using precision, recall, and F1.

    Inputs
    ------
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.

    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
    precision = precision_score(y, preds, zero_division=1)
    recall = recall_score(y, preds, zero_division=1)
    return precision, recall, fbeta


def compute_metrics_on_slices(
        data: pd.DataFrame,
        slice_on: str,
        y: np.array,
        preds: np.array) -> pd.DataFrame:
    """
    Validates the trained machine learning model using precision, recall, and
    F1, keeping the value of a given feature fixed

    Inputs
    ------
    data: pd.DataFrame
        Original data used to extract y
    slice_on: str
        Feature to test the model on
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.

    Returns
    -------
    report: pd.DataFrame
        The metrics from compute_model_metrics to each category from slice_on
        passed
    """
    l_rtn = []
    i_size = len(y)
    for category in data[slice_on].unique():
        if not isinstance(category, str):
            raise ValueError('The categories should be all strings')
        na_b_filters = (data[slice_on] == category).values
        t_metrics = compute_model_metrics(y[na_b_filters], preds[na_b_filters])
        d_this_return = {'slice_on': slice_on, 'category': category}
        d_this_return['sample_size'] = (np.sum(na_b_filters) * 1.0) / i_size
        d_this_return['precision'] = t_metrics[0]
        d_this_return['recall'] = t_metrics[1]
        d_this_return['fbeta'] = t_metrics[2]
        l_rtn.append(d_this_return)

    return pd.DataFrame(l_rtn).set_index(['slice_on', 'category'])


def inference(model, X):
    """ Run model inferences and return the predictions.

    Inputs
    ------
    model : python object
        Trained machine learning model.
    X : np.array
        Data used for prediction.

    Returns
    -------
    preds : np.array
        Predictions from the model.
    """
    return model.predict(X)
