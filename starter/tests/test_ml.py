'''
Implement tests to ml model

Author: ucaiado
Date: February 13th, 2022
'''

import sys
import pathlib
import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

sys.path.append(str(pathlib.Path.cwd() / 'starter' / 'starter' ))
from ml.model import (
    train_model,
    compute_model_metrics,
    inference,
    compute_metrics_on_slices)


@pytest.fixture
def model_data():
    x_train = np.array([[0.0, 1.0], [2.0, 3.0]])
    y_train = np.array([[1.0], [0.0]])
    this_model = train_model(x_train, y_train)

    return this_model, x_train, y_train


def test_model_type(model_data):
    this_model, x_train, y_train = model_data

    assert isinstance(this_model, RandomForestClassifier)


def test_predict_function(model_data):
    this_model, x_train, y_train = model_data
    y_pred = inference(this_model, x_train)

    assert sum(abs((y_train - y_pred.reshape(-1, 1))))[0] < 1e-6


def test_computes_performance_on_model_slices(model_data):
    this_model, x_train, y_train = model_data
    data = pd.DataFrame(x_train, columns=['A', 'B'])

    # this function should work only with categotical features
    try:
        df_output = compute_metrics_on_slices(
            data=data,
            slice_on='A',
            y=y_train,
            preds=np.array([1.0, 1.0]))
        assert False
    except ValueError:
        assert True

    data['A'] = data['A'].astype(str)
    df_output = compute_metrics_on_slices(
        data=data,
        slice_on='A',
        y=y_train,
        preds=np.array([1.0, 1.0]))


    assert isinstance(df_output, pd.DataFrame)
    assert abs((df_output['recall'] == 1).sum() - 2) < 1e-6


def test_metrics_output():
    t_out = compute_model_metrics(
        np.array([1.0, 1.0]),
        np.array([1.0, 1.0])
        )
    for f_metric in t_out:
        assert abs(f_metric - 1.0) < 1e-6