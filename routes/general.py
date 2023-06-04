from fastapi import APIRouter
from bson import ObjectId

from db import get_db,c2j

app = APIRouter(
    tags=["General"]
)


db = get_db()







@app.get("/sNames")
async def post_student_names():
    students = db["parents"]
    
    name = students.find({}, {"_id":0,"name": 1, "username": 1})
    return c2j(name)

        
    
    



@app.post("/dNames")
async def post_doctor_names():
    doctors = db["doctors"]
    names = doctors.find({}, {"_id":0,"name": 1, "username": 1})
    return c2j(names)



@app.post("/aNames")
async def post_admin_names():
    admins = db["admins"]
    names =  admins.find({}, {"_id":0,"name": 1, "username": 1})
    return c2j(names)



@app.post("/sDetails")
async def post_student_details(id: str):
    students = db["parents"]
    s =  students.find_one({"username": id},{"_id":0})
    return s



@app.post("/dDetails")
async def post_doctor_details(id: str):
    doctors = db["doctors"]
    d = doctors.find_one({"username": id},{"_id":0})
    return d


@app.post("/aDetails")
async def post_admin_details(id: str):
    admins = db["admins"]
    a = admins.find_one({"username": id},{"_id":0})
    return a

