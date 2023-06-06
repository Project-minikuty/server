import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
connection_string = os.getenv('ATLAS_URI')
client = MongoClient(connection_string)

db = client["medlab"]
print("Database connection established")


def c2j(name):
    names = []
    for n in name:
        d = dict(n)
        if d.get("_id"):
            d["_id"]=str(d["_id"])
        names.append(d)
    return names


def get_db():
    return db
