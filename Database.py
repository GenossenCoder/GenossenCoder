import certifi
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId

def Connect():
    connection_string = "mongodb+srv://adim:WknSllcgkPnBuuR1@cluster0.uw8iy.mongodb.net/Discord?retryWrites=true&w=majority"
    client  = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client['Discord']
    Events = db.Event
    return Events

def createPoll(text,title,pollType,competetors,deadline):  
    Events=Connect();
    if pollType=="multi":
        Event_single = {
        "title": title,
        "text": text,
        "competetors":competetors,
        "createdAt": datetime.utcnow(),
        "deadline": datetime.now() + timedelta(hours=deadline-1),
        } 
        #appending competetors to the dictonary
        for i in range(len(competetors)):
            Event_single[competetors[i]]=[]
    Events.insert_one(Event_single)

def addVote(id,vote,name):
    Events=Connect();
    Events.update_one({"_id" :ObjectId(id)},{"$push":{vote:name}})
    return("sucessfull")


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
#running()
#addVote("6204fa9bb6436cbdfc1c9e8d","Jasmin","du")
#createPoll("text","title","multi",["Zombie", "Jasmin","Olaf","Clemens"],9)S