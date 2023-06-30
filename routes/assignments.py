from fastapi import APIRouter

from db import c2j, get_db

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
