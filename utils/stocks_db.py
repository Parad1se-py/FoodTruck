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

import os

from dotenv import load_dotenv
from pymongo import MongoClient

from data import *


load_dotenv()

cluster = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.mosbb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["foodtruck"]


# Stocks data related functions
def get_stock_data(name):
    return stocks[name]

def update_stock_count(name, count):
    stocks[name]['amt'] += count

def update_stock_price(name, count):
    stocks[name]['price'] += count

def update_stock_type(name, type):
    stocks[name]['type'] = type

def update_stockup_count(name, count):
    stocks[name]['bought'] += count

def set_stockup_count(name, count):
    stocks[name]['bought'] = count

# User DB for stocks related functions
def add_stock(user, item, amount=1):
    collection.update_one(
        {"_id": user.id},
        {"$inc": {f"stocks.{item}": amount}}
    )

def check_for_stock(user_id, item):
    d = collection.find_one({"_id": user_id})
    try:
        if d["stocks"][item] >= 1:
            return True
    except Exception:
        return False

def stock_count(user, item):
    if check := check_for_stock(user, item):
        d = collection.find_one({"_id": int(user.id)})
        return d['stocks'][item]
    else:
        return 0
