'''
Train a model in Census data

Author: ucaiado
Date: February 13th, 2022
'''

# Add the necessary imports for the starter code.
import pathlib
import joblib
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

from ml.data import process_data
from ml.model import (train_model, compute_model_metrics, inference)


# set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

# Add code to load in the data.
data = pd.read_csv(pathlib.Path.cwd() / 'data' / 'census.cleaned.csv')

# Optional enhancement, use K-fold cross validation instead of a train-test split.
train, test = train_test_split(data, test_size=0.20)
logger.info('... split data')


cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]

X_train, y_train, encoder_train, lb_train = process_data(
    train,
    categorical_features=cat_features,
    label="salary",
    training=True
)

# Proces the test data with the process_data function.
X_test, y_test, encoder_test, lb_test = process_data(
    test,
    categorical_features=cat_features,
    label="salary",
    training=False,
    encoder=encoder_train,
    lb=lb_train
)

logger.info('... pre-process data to training/testing')

# Train  model
train_clf = train_model(X_train, y_train)
y_train_preds = inference(train_clf, X_train)
t_train_rtns = compute_model_metrics(y_train, y_train_preds)
logger.info('... training the model')

# test_clf = train_model(X_test, y_test)
y_test_preds = inference(train_clf, X_test)
t_test_rtns = compute_model_metrics(y_test, y_test_preds)
logger.info('... test the model created')

# save model
joblib.dump(train_clf, pathlib.Path.cwd() / 'model' / 'model.pkl')
joblib.dump(encoder_train, pathlib.Path.cwd() / 'model' / 'encoder.pkl')
logger.info('... save the model created')

# log metrics
precision_train, recall_train, fbeta_train = t_train_rtns
precision_test, recall_test, fbeta_test = t_test_rtns
logger.info('... calculate metrics')
for s_name, (precision ,recall, fbeta) in zip(
    ["Training", "Test"], [t_train_rtns, t_test_rtns]):
    logger.info(
        f"=========== On {s_name} data"
        f":\n\tPrecision: {precision:.4f}"
        f"\n\tRecall: {recall:.4f}"
        f"\n\tF1 score: {fbeta:.4f}")
    pass

