from pydantic import BaseModel
from typing import List,Dict,Optional

class Patient(BaseModel):
    name : str
    age : int
    weight : float
    married : Optional[bool]
    contact : Dict[str ,str]
    allergies : Optional[list[str]] = None

def add_name(patient : Patient) :
    print(patient.name)
    print(patient.age)
    print("added")
    print(patient.allergies)


patient_info = {'name' : 'sourav','age' : 30,'weight' :67.5,'married':1,'contact':{'email':'sou@gmail.com','phone_no':'8776655'}
                ,'allergies':['dust','pollen']}

patient1 = Patient(**patient_info)

add_name(patient1)

