import pymongo
import json
import sys

# Local Files
sys.path.append("..")
from scripts import settings

client = pymongo.MongoClient(settings.mongo_server, settings.mongo_id)
db = client[settings.mongo_client]
db.authenticate(settings.mongo_user, settings.mongo_pass)

def push(query, datatype, data):
    d = db.logs.find_one({'query': query})
    if d is not None:
        data = json.loads(d[datatype])+[data]
        d[datatype] = json.dumps(data)
        db.logs.save(d)
    else:
        db.logs.insert_one({'query': query, datatype: json.dumps([data])})

def load(query, datatype):
    d = db.logs.find_one({'query': query})
    return json.loads(d[datatype])