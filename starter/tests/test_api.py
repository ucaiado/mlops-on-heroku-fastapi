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


# def test_api_post_infer_income_level_zero():
#     features = {
#         'age': 42,
#         'workclass': 'Private',
#         'fnlgt': 159449,
#         'education': 'Bachelors',
#         'education-num': 13,
#         'marital-status': 'Married-civ-spouse',
#         'occupation': 'Exec-managerial',
#         'relationship': 'Husband',
#         'race': 'White',
#         'sex': 'Male',
#         'capital-gain': 5178,
#         'capital-loss': 0,
#         'hours-per-week': 40,
#         'native-country': 'United-States'}

#     r = client.post("/infer_income", json=features)

#     assert r.status_code == 200
#     assert r.json() == {"prediction": 1}
