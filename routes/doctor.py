from fastapi import APIRouter
from bson import ObjectId
from db import  get_db
from datetime import date, datetime


db = get_db()
app = APIRouter(
    tags=["Doctor"],
)

@app.get("/patients")
def patient_list():
    d = db["doctors"]
    p = d.find({"patients":1,"_id":0})
    return p
@app.get("/appointments")
def appointment_list(date_ :str = str(datetime.now().date())):

    return date_
