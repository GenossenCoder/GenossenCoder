import certifi
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from TOKEN import database_token

def Connect():
    connection_string = database_token
    client  = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client['Discord']
    Events = db.Event
    return Events

def createPoll(text,title,pollType,competitors,deadline):  
    Events=Connect();
    if pollType=="multi":
        Event_single = {
        "title": title,
        "text": text,
        "competitors":competitors,
        "createdAt": datetime.utcnow(),
        "deadline": datetime.now() + timedelta(hours=deadline-1),
        } 
        #appending competetors to the dictonary
        for i in range(len(competitors)):
            Event_single[competitors[i]]=[]
    Events.insert_one(Event_single)
    return "Success"

def addVote(id,vote,name):
    Events=Connect();
    Events.update_one({"_id" :ObjectId(id)},{"$push":{vote:name}})
    return("Success")


def getPoll(id):
    Events=Connect()
    Poll=Events.find_one({"_id" :ObjectId(id)})
    return Poll


def deletePoll(id):
    Events=Connect()
    Events.delete_one({"_id" :ObjectId(id)})
    return "Success"
    

def running():
    Events=Connect()
    Polls=Events.find()
    runningPolls=[]
    for i in Polls:
        if i['deadline'] > datetime.utcnow():
            runningPolls.append(i['_id'])
    return runningPolls
