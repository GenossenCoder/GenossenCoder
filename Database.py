import pymongo
from pymongo import MongoClient

connection_string = "mongodb+srv://adim:WknSllcgkPnBuuR1@cluster0.uw8iy.mongodb.net/Discord?retryWrites=true&w=majority"

def ConnectToMongo(string):
    client = MongoClient(string)
    return client["Discord"]

dbname= ConnectToMongo(connection_string)
collection_name = dbname["Events"]

Event_single = {
"name": "zombie stinkt",
"text": "Emil ist genauso dumm",
"yes" : ["Michael", "ClemensDerKek"],
"no": ["Siegfried", "Sybille"],
"date": "12.03.2012"
}
Event_multi = {
"name": "zombie stinkt",
"text": "Emil ist genauso dumm",
}

collection_name.insert_many([Event_single,Event_multi])