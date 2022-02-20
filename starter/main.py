'''
Implement API to fetch data from the model created

Author: ucaiado
Date: February 20th, 2022
'''

# Put the code for your API here
import pathlib
import joblib
from fastapi import FastAPI
from pydantic import (BaseModel, Field)

app = FastAPI()


MODEL = joblib.load(pathlib.Path.cwd() / 'starter' / 'model' / 'model.pkl')
ENCONDER = joblib.load(pathlib.Path.cwd() / 'starter' / 'model' / 'encoder.pkl')
CAT_FEATURES = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]


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
    import pdb; pdb.set_trace()
    return {}
