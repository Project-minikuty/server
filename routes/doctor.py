from fastapi import APIRouter
from bson import ObjectId
from db import c2j, get_db
from datetime import date, datetime

from schemas import cAssignBody


db = get_db()
app = APIRouter(
    tags=["Doctor"],
)


@app.get("/patients")
def patient_list(username: str):
    d = db["doctors"]
    p = d.find_one({"username": username}, {"patients": 1, "_id": 0})
    if len(p):
        query = {"username": {"$in": p["patients"]}}
        doctors = db["users"]
        names = doctors.find(query, { "name": 1, "username": 1,"suspended":1})
    
        return c2j(names) 
    else:
        return []
    


@app.get("/dappointments")
def doctors_appointment_list(username: str, aType: str, date_: str = str(datetime.now().date())):
    d = db[aType]
    p = d.find({
        "doc": username,
        "date": date_
    }, {"_id": 0})
    return c2j(p)


@app.get("/pappointments")
def patients_appointment_list(username: str, aType: str, date_: str = str(datetime.now().date())):
    d = db[aType]
    p = d.find({
        "pat": username,
        "date": date_
    }, {"_id": 0})
    return c2j(p)


@app.post("/cAssignment")
def create_new_assignment(body: cAssignBody):
    a = db['assignments']
    print(body)
    b = {
        "name" : body.name,
        "description" : body.desc,
        "pat":body.pat,
        "doc":body.doc,
        "docE":body.docE,
        "patE":body.patE,
        "files" : body.files,
        "status":False
    } if body.files else {
        "name" : body.name,
        "description" : body.desc,
        "pat":body.pat,
        "doc":body.doc,
        "docE":body.docE,
        "patE":body.patE,
        "status":False
        
    }
    res = a.insert_one(b)
    if res.acknowledged:
        return ({"message": "Data inserted successfully!",
                 "success": True})
    else:
        return({
            "message": f"Error inserting data! {res}",
            "success": False
        })


@app.post("/cPrescription")
def create_Prescription():

    return {}
