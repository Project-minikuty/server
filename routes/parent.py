from fastapi import APIRouter
from bson import ObjectId
from db import  c2j, get_db
from datetime import date, datetime


db = get_db()
app = APIRouter(
    tags=["Parent"],
)

@app.get("/assignments")
def get_assignments(username :str):
    return {}