from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="id of the patient.", examples="P001")] 
    name: Annotated[str, Field(..., description="name of the patient.")]
    city: Annotated[str, Field(..., description="name of the city")]
    age: Annotated[str, Field(..., description="age of the patient.")]
    gender: Annotated[str, Literal['male', 'female', 'others'], Field(..., description="gender of   patient", examples="male")]
    height: Annotated[float, Field(...,gt=0 , description="height of the patient.", examples="176")]
    weight: Annotated[float, Field(...,gt=0, description="weight of the patient.", examples="70")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/ (self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.9:
            return 'Underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Overweight'



def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

#THE ENDPOINTS

@app.get('/')
def hello():
    return{'message':'patient management System API'}

@app.get("/about")
def about():
    return{"message":"A fully functional API for patient record"}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(...,description = 'ID of the patient in DB', example= 'P001')):
    # load all the patient 
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient not found')

@app.get('/sort')
def sort_patients(sort_by: str =Query(..., description='sort on the basis of height, weight'),
                order: str = Query('asc', description='sort on the basis of order')):
    valid_fields = ['height', 'weight']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid field, select from {valid_fields}')

    valid_orders = ['asc', 'dsc']
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail='Invalid order, select from {valid_orders}')

    data = load_data()

    sort_order = True if order=='dsc' else False

    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by,0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #load the existing data
    data = load_data()

    #cheack if it already exists?
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exists!')

    #add new patient in the data
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save into the json file 
    save_data(data)

    return JSONResponse(
        status_code=201, 
        content={'message': 'new Patient is succesfully created!'})