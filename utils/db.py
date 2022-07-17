from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://teamFrixionOne:GWKRO8CetoiggeAI@cluster0.mosbb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["foodtruck"]

def register(user):
    """Register a user."""
    post = {"_id": int(user.id), "wallet": 500, "pizzeria": "None", "ingredients": {}, "active":[], "level": 0, "level_l": 0, "badges":[]}
    collection.insert_one(post)
    return True

def check_acc(id):
    """Check if a user is registered in the database"""
    user = collection.find_one({"_id": id})
    return bool(user)

def update_data(id, mode, amount):
    """Update any data on the user"""
    collection.update_one({"_id" : id}, {"$inc" : {str(mode): amount}})