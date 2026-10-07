from pydantic import BaseModel, EmailStr,AnyUrl,Field
from typing import List,Optional
class Patient(BaseModel):
    name: str
    age: int = Field(lt=90)         #FIELD
    weight: float = 60              #DEFAULT VALUE
    height: float                   #MANDATORY
    married: Optional[bool] = None  #OPTIONAL
    allergies: List[str]

    #DATA VALIDATION
    email: EmailStr
    linkedin_Url: AnyUrl = None
    

def insert_patient_data(patient1: Patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.weight)
    print(patient1.height)
    print(patient1.married)
    print(patient1.allergies)
    print('inserted data')

patient_info = {'name': 'sujal', 'age': 20, 'weight': 69.5, 'height': 5.9, 'married': False, 'allergies': ['pollen', 'peenuts'], 'email': 'abc@gmail.com' }

patient1 = Patient(**patient_info)
insert_patient_data(patient1)