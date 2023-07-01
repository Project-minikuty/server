
from pydantic import BaseModel
from bson import ObjectId


class validateBody(BaseModel):
    username: str | None = "hello"
    class Config:
        orm_mode = True


class cAssignBody(BaseModel):
    name :str
    desc:str
    pat:str
    doc:str
    files:list | None =None
    class Config:
        orm_mode = True

class sAssBody(BaseModel):
    id_: str
    name: str
    comments: str
    doc: str
    files: list | None =None
    pat: str

class createUserBody(BaseModel):
    username: str
    password: str
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
    class Config:
        orm_mode = True
class onAppoBody(BaseModel):
    date :str
    doc:str
    pat:str
    room:str
    time: str
class ofAppoBody(BaseModel):
    date :str
    doc :str
    pat :str
    time: str
class updateUserBody(BaseModel):
    username: str
    password: str
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
    class Config:
        orm_mode = True
