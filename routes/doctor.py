from fastapi import APIRouter
from bson import ObjectId
from db import  c2j, get_db
from datetime import date, datetime


db = get_db()
app = APIRouter(
    tags=["Doctor"],
)

@app.get("/patients")
def patient_list(username :str):
    d = db["doctors"]
    p = d.find_one({"username":username},{"patients":1,"_id":0})
    return p["patients"] if len(p) else {}

@app.get("/appointments")
def appointment_list(username:str,date_ :str = str(datetime.now().date())):
    d = db["doctors"]
    p = d.find_one({"username":username},{f"appointments.{date_}":1,"_id":0})
    return p["appointments"].get(date_,[]) if len(p) else {}

@app.post("/cPrescription")
def create_Prescription():

    return {}


