import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
connection_string = os.getenv('ATLAS_URI')
client = MongoClient(connection_string)

db = client["medlab"]
print("Database connection established")


def c2j(cursor) -> list[dict]:
    list = []
    for n in cursor:
        d = dict(n)
        if d.get("_id"):
            d["_id"]=str(d["_id"])
        list.append(d)
    return list
def d2j(d):
    
    if d.get("_id"):
        d["_id"]=str(d["_id"])
    
    return d


def get_db():
    return db
