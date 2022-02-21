'''
Implement API to fetch data from the model created

Author: ucaiado
Date: February 20th, 2022
'''

# Put the code for your API here
import os
import pathlib
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import (BaseModel, Field)

from starter.ml.data import process_data
from starter.ml.model import inference


# set up FastAPI app
app = FastAPI()


# enable Heroku to use DVC
if "DYNO" in os.environ and os.path.isdir(".dvc"):
    os.system("dvc config core.no_scm true")
    if os.system("dvc pull") != 0:
        exit("dvc pull failed")
    os.system("rm -r .dvc .apt/usr/lib/dvc")


# define root path
root_path = pathlib.Path.cwd() / 'starter' / 'model'
if not root_path.is_dir():
    root_path = pathlib.Path.cwd() / 'model'


# load model
MODEL = joblib.load(root_path / 'model.pkl')
ENCONDER = joblib.load(root_path / 'encoder.pkl')
CAT_FEATURES = [
    "workclass",
    "education",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native_country",
]


# define data structure
class Features(BaseModel):
    age: int
    workclass: str
    fnlgt: int
    education: str
    education_num: int = Field(alias='education-num')
    marital_status: str = Field(alias='marital-status')
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int = Field(alias='capital-gain')
    capital_loss: int = Field(alias='capital-loss')
    hours_per_week: int = Field(alias='hours-per-week')
    native_country: str = Field(alias='native-country')


# define endpoints
@app.get("/")
async def get_root():
    '''
    GET on the root giving a welcome message
    '''
    return {"message": ("Welcome to the income level classifier API !! "
                        "Please, visit /docs to further instructions.")}


@app.post("/infer_income")
async def post_infer_income_level(features: Features):
    '''
    POST that does model inference using the features passed
    '''
    df_this_data = pd.DataFrame(features).set_index(0).T

    x_data, _, _, _ = process_data(
        df_this_data,
        categorical_features=CAT_FEATURES,
        training=False,
        encoder=ENCONDER,
    )

    na_inference = inference(MODEL, x_data)

    return {"is_above_50k": int(na_inference[0])}
