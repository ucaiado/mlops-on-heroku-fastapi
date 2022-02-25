#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement simple api test


@author: ucaiado

Created on 02/25/2022
"""

# import libraries
import argparse
import textwrap
import requests
import pathlib
import json


if __name__ == '__main__':
    s_txt = '''\
            Tests the app created
            --------------------------------
            The file heroku_output.txt should exist
            '''
    # include and parse variables
    obj_formatter = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=obj_formatter, description=textwrap.dedent(s_txt))

    args = parser.parse_args()

    # check if the file with heroku app address has been created
    path_file = pathlib.Path.cwd() / 'heroku_output.txt'
    s_err = 'All steps in the Makefile should be performed before running the'
    s_err += ' tests'
    assert path_file.is_file(), s_err

    # recover heroku app address
    s_last_app = open(path_file).read()
    s_last_app = s_last_app.split(' | ')[0]
    s_last_app = s_last_app.split('//')[1].split('.heroku')[0]

    heroku_url = f"https://{s_last_app}.herokuapp.com/infer_income"

    print(heroku_url)

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

    r = requests.post(heroku_url, json=features)

    assert r.status_code == 200
    assert r.json() == {"is_above_50k": 1}

    print('\n======= POST =========')
    print(json.dumps(features, indent=4))

    print('\n\n===== RESPONSE =======')
    print(json.dumps(r.json(), indent=4))
