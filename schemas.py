
from pydantic import BaseModel 
from bson import ObjectId
class validateBody(BaseModel):
    username : str | None ="hello"

class createUserBody(BaseModel):
    username : str
    password : str
    name: str
    type: int
    age: int | None = None
    height: str | None = None
    weight: str | None = None
    gender: str | None = None
    dob: str | None = None
    bloodGroup: str | None = None
    guardianName: str | None = None
    occupation: str | None = None
    phoneNumber: str | None = None
    address: str | None = None