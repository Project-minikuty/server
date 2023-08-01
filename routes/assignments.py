from bson import ObjectId
from fastapi import APIRouter
from schemas import sAssBody
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

@app.get("/dAssignments/{username}")
def get_sassignment_list_for_parent(username :str):
    ass = db["assignmentSub"]
    res = ass.find({"doc":username})
    res = c2j(res)
    return res if len(res) else {}

@app.get('/assData/{_id}')
def get_ass_data(_id):
    a=db["assignments"]
    res = a.find_one({"_id":ObjectId( _id)})
    return d2j(res)

@app.post('/grade/{_id}')
def grade_ass_data(_id):
    a=db["assignmentSub"]
    res = a.update_one({"_id":ObjectId( _id)},{"$set":{"graded":True}})
    if res.acknowledged:
        return {"success":True}
    else:
        return {"success":False}

@app.get('/sassData/{_id}')
def get_sass_data(_id):
    a=db["assignmentSub"]
    res = a.find_one({"_id":ObjectId( _id)})
    return d2j(res)

@app.post('/sAss')
def sub_assignment(body : sAssBody):
    a=db["assignmentSub"]
    bd = {
        "name":body.name,
        "comments":body.comments,
        "_id":ObjectId(body.id_),
        "doc":body.doc,
        "pat":body.pat,
        "docE":body.docE,
        "patE":body.patE,
        "files":body.files,
        "graded":False
    } if body.files else {
        "name":body.name,
        "comments":body.comments,
        "_id":ObjectId(body.id_),
        "doc":body.doc,
        "pat":body.pat,
        "docE":body.docE,
        "patE":body.patE,
        "graded":False
        
    }
    res = a.insert_one(bd)
    print(res)
    if res.acknowledged:
        b=db["assignments"]
        b.update_one({"_id":ObjectId(body.id_)},{"$set":{"status":True}})
        return {"message":"submitted","success":True}
    else :
        return {"error" :"something went wrong","succes":False}
    