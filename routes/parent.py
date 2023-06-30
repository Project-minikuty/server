from fastapi import APIRouter
from bson import ObjectId
from db import c2j, get_db
from datetime import date, datetime

db = get_db()
app = APIRouter(
    tags=["Parent"],
)

@app.get("/assignments")
def get_assignments(username: str):
    return "under construction"

@app.post("/createAppointment")
def create_appointment(doctor_username: str, time: str, date: date):
    appointment_data = {
        "doctor_username": doctor_username,
        "time": time,
        "date": date,
    }
   

    return {"message": "Appointment created successfully"}

