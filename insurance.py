from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal
import pandas as pd
import pickle 

with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()