from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://teamFrixionOne:GWKRO8CetoiggeAI@cluster0.mosbb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["foodtruck"]

def register(user):
    """Register a user."""
    post = {"_id": int(user.id), "wallet": 500, "pizzeria": "None", "inv": {}, "active":[], "level": 0, "level_l": 0, "badges":[]}
    collection.insert_one(post)
    return True

def check_acc(id):
    """Check if a user is registered in the database"""
    user = collection.find_one({"_id": id})
    return bool(user)

def update_data(id, mode, amount):
    """Update any data on the user"""
    collection.update_one({"_id" : id}, {"$inc" : {str(mode): amount}})
    
def get_all_data():
    """Get all users' data"""
    return collection.find({})

def get_user_data(user):
    """Get a specific user's data"""
    return collection.find_one({"_id": user.id})


async def update_l(user, points):
    """Update a user's level"""
    collection.update_one({"uid": user.id}, {"$inc": {"level_l": int(points)}})
    lvl = collection.find_one({"uid": user.id})["level"]
    lvll = collection.find_one({"uid": user.id})["level_l"]

    if lvl == 0:
        if lvll >= 5:
            collection.update_one({"uid": user.id}, {"$set": {"level": 1}})
            collection.update_one({"uid": user.id}, {"$set": {"level_l": 0}})
    elif lvll >= lvl*10:
        collection.update_one({"uid": user.id}, {"$set": {"level": lvl+1}})
        collection.update_one({"uid": user.id}, {"$set": {"level_l": 0}})
        
def add_item(user, item, amount=1):
    collection.update_one(
        {"uid": user.id},
        {"$inc": {f"inv.{item}": int(amount)}}
    )
    
def check_for_item(user, item):
    d = collection.find_one({"uid": int(user.id)})
    try:
        if d["inv"][item] >= 1:
            return True
    except Exception:
        return False
    
def check_for_active(user, item):
    d = collection.find_one({"uid": int(user.id)})
    if len(d['active']) == 0:
        return None
    try:
        if item.lower() in d['active']:
                return True
    except Exception:
        return False

def add_active(user, item):
    collection.update_one(
        {"uid": user.id},
        {"$push": { "active": item}}
    )
    
def item_count(user, item):
    if check := check_for_item(user, item):
        x = collection.find_one({"uid": int(user.id)})
        return x['inv'][item]
    else:
        return 0