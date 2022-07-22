# -*- coding: utf-8 -*-
# Copyright (c) 2022 Parad1se-py

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json

from pymongo import MongoClient

with open("configuration.json", "r") as config: 
	data = json.load(config)
	username = data["mongo_username"]
	password = data["mongo_pass"]

cluster = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.mosbb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["foodtruck"]

def register(user):
    """Register a user."""
    post = {"_id": int(user.id), "cash": 500, "streak":0, "name": None, "inv": {}, "active":{}, "dishes":{}, "level": 1, "level_l": 1, "badges":[]}
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

def get_user_data(id):
    """Get a specific user's data"""
    return collection.find_one({"_id": id})


async def update_l(user, points):
    """Update a user's level"""
    collection.update_one({"_id": user.id}, {"$inc": {"level_l": int(points)}})
    lvl = collection.find_one({"_id": user.id})["level"]
    lvll = collection.find_one({"_id": user.id})["level_l"]

    if lvl == 0:
        if lvll >= 5:
            collection.update_one({"_id": user.id}, {"$set": {"level": 1}})
            collection.update_one({"_id": user.id}, {"$set": {"level_l": 0}})
    elif lvll >= lvl*10:
        collection.update_one({"_id": user.id}, {"$set": {"level": lvl+1}})
        collection.update_one({"_id": user.id}, {"$set": {"level_l": 0}})
        
def add_item(user, item, amount=1):
    collection.update_one(
        {"_id": user.id},
        {"$inc": {f"inv.{item}": int(amount)}}
    )

def purge_item(id, item, amount):
    collection.update_one(
        {"_id": id},
        {"$unset": {f"inv.{item}": amount}}
    )

def remove_item(id, item:str, amount:int=1):
    if item_count(id, item) == amount:
        purge_item(id, item, amount)
    else:
        collection.update_one(
            {"_id": id},
            {"$unset": {f"inv.{item}": amount}}
        )
        
def add_dish(user, item, amount=1):
    collection.update_one(
        {"_id": user.id},
        {"$inc": {f"dishes.{item}": int(amount)}}
    )

def purge_dish(id, item, amount):
    collection.update_one(
        {"_id": id},
        {"$unset": {f"dishes.{item}": amount}}
    )

def remove_dish(id, item:str, amount:int=1):
    if item_count(id) == amount:
        purge_dish(id, item, amount)
    else:
        collection.update_one(
            {"_id": id},
            {"$unset": {f"dishes.{item}": amount}}
        )

def check_for_item(id, item):
    d = collection.find_one({"_id": int(id)})
    try:
        if d["inv"][item] >= 1:
            return True
    except Exception:
        return False
    
def check_for_dish(id, item):
    d = collection.find_one({"_id": int(id)})
    try:
        if d["dishes"][item] >= 1:
            return True
    except Exception:
        return False

def add_active(user, item, amount=1):
    collection.update_one(
        {"_id": user.id},
        {"$inc": {f"active.{item}": int(amount)}}
    )

def remove_active(id, item:str, amount:int=1):
    collection.update_one(
        {"_id": id},
        {"$unset": {f"active.{item}": amount}}
    )
    
def item_count(id, item):
    if _ := check_for_item(id, item):
        x = collection.find_one({"_id": int(id)})
        return x['inv'][item]
    else:
        return 0
    
def dish_count(id, item):
    if _ := check_for_dish(id, item):
        x = collection.find_one({"_id": int(id)})
        return x['inv'][item]
    else:
        return 0