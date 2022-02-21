'''
Implement tests to the API

Author: ucaiado
Date: February 20th, 2022
'''
import sys
import pathlib
from fastapi.testclient import TestClient

sys.path.append(str(pathlib.Path.cwd() / 'starter'))
from main import app


client = TestClient(app)


def test_api_get_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": ("Welcome to the income level classifier "
                        "API !! Please, visit /docs to further instructions.")}


def test_api_post_infer_income_level_zero():
    features = {
        'age': 39,
        'workclass': 'State-gov',
        'fnlgt': 77516,
        'education': 'Bachelors',
        'education-num': 13,
        'marital-status': 'Never-married',
        'occupation': 'Adm-clerical',
        'relationship': 'Not-in-family',
        'race': 'White',
        'sex': 'Male',
        'capital-gain': 2174,
        'capital-loss': 0,
        'hours-per-week': 40,
        'native-country': 'United-States'}

    r = client.post("/infer_income", json=features)

    assert r.status_code == 200
    assert r.json() == {"is_above_50k": 0}


def test_api_post_infer_income_level_one():
    features = {
        'age': 52,
        'workclass': 'Self-emp-not-inc',
        'fnlgt': 209642,
        'education': 'HS-grad',
        'education-num': 9,
        'marital-status': 'Married-civ-spouse',
        'occupation': 'Exec-managerial',
        'relationship': 'Husband',
        'race': 'White',
        'sex': 'Male',
        'capital-gain': 0,
        'capital-loss': 0,
        'hours-per-week': 45,
        'native-country': 'United-States'}

    r = client.post("/infer_income", json=features)

    assert r.status_code == 200
    assert r.json() == {"is_above_50k": 1}
