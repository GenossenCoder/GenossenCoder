import certifi
from pymongo import MongoClient
from datetime import datetime, timedelta

def Connect():
    connection_string = "mongodb+srv://adim:WknSllcgkPnBuuR1@cluster0.uw8iy.mongodb.net/Discord?retryWrites=true&w=majority"
    client  = MongoClient(connection_string, tlsCAFile=certifi.where())
    db = client['Discord']#
    Events = db.Event
    return Events

def createPoll(text,title,pollType,competetors,deadline):
    
    Events=Connect();
    votes=[]
    if pollType=="multi":
        for i in competetors:
           votes.append([])
        Event_single = {
        "title": title,
        "text": text,
        "competetors":competetors,
        "createdAt": datetime.utcnow(),
        "deadline":datetime.now() + timedelta(hours=deadline-1),
        "votes": votes
        }
        
    print(Events)
    Events.insert_one(Event_single)