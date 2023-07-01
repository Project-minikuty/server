from bson import ObjectId
from fastapi import APIRouter

from db import c2j, d2j, get_db

db = get_db()
app = APIRouter(
    tags=["Assignments"],
)

@app.get("/pAssignments/{username}")
def get_assignment_list_for_parent(username :str):
    ass = db["assignments"]
    res = ass.find({"pat":username})
    res = c2j(res)
    return res if len(res) else {}

@app.get('/assData/{_id}')
def get_ass_data(_id):
    a=db["assignments"]
    res = a.find_one({"_id":ObjectId( _id)})
    return d2j(res)