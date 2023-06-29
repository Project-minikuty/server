from fastapi import APIRouter
from bson import ObjectId

from db import get_db, c2j

app = APIRouter(
    tags=["General"]
)


db = get_db()




@app.get("/Names")
async def get_list_of_names(type :int):
    if 0<type<4:
        cons = {"type":type}
    else :
        cons={}
    doctors = db["users"]
    names = doctors.find(cons, { "name": 1, "username": 1,"suspended":1})
    return c2j(names)





@app.get("/sDetails")
async def post_student_details(id: str):
    students = db["parents"]
    s = students.find({"_id": ObjectId(id)})
    s=c2j(s)
    
    return s[0] if len(s) else "user not found"


@app.get("/dDetails")
async def post_doctor_details(id: str):
    doctors = db["doctors"]
    d = doctors.find({"_id": ObjectId(id)})
    d=c2j(d)
    return d[0] if len(d) else "user not found"


@app.get("/aDetails")
async def post_admin_details(id: str):
    admins = db["admins"]
    a = admins.find_one({"_id": ObjectId(id)})
    a=c2j(a)
    return a[0] if len(a) else "user not found"
