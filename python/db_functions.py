import pymongo
from bson import ObjectId
from datetime import datetime, timezone
client = pymongo.MongoClient("mongodb+srv://koff:koffroxx@cluster0.gtqq3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.koff

user_col = db.users

tests_col = db.tests

web_col = db.web

def register_user(user):
    print(user)
    user_object ={
        "user_id": user.uuid,
        "password": user.password,
        "age": user.age
    }
    inserted_id = user_col.insert_one(user_object).inserted_id
    return { 
        "message": "success",
        "token": str(inserted_id)
    }


def login_user(user):
    user_object = user_col.find_one({"user_id":user.uuid})
    if(user_object):
        if(user.password == user_object["password"]):
            return {
                "message":"success",
                "token": str(user_object["_id"])
            }
        else:
            return {
                "message":"Passwords did not match."
            }
    else:
        return {
                "message":"No user found."
            }

def create_test(predictions, token):
    new_test ={
        "user_token": token,
        "results": predictions
    }
    inserted_id = tests_col.insert_one(new_test).inserted_id
    # add this record to the block chain
    return inserted_id

def get_home_info(token):
    user_object = user_col.find_one({"_id":ObjectId(token)})
    last_test = list(tests_col.find({"user_token":token}).sort("_id",-1).limit(1))
    time_stamp = last_test[0]["_id"].generation_time
    is_avail = (datetime.now(timezone.utc)- time_stamp).total_seconds() >= 86400
    response_data ={
        "test_avail": is_avail,
        "last_test": last_test[0]["results"]["verdict"] == 'NOT-ILL',
        "last_test_timestamp": time_stamp,
        "uuid": user_object["user_id"],
        "country": "Australia",
        "age": user_object["age"]
    }
    return (response_data)


def get_history(token):
    last_5_tests = list(tests_col.find({"user_token":token}).sort("_id",-1).limit(5))
    # print(datetime.timestamp(last_5_tests[0]["_id"].generation_time))
    polished_data = []
    for test in last_5_tests:
        polished_data.append({
            "timestamp": test["_id"].generation_time,
            "result": test["results"]["verdict"] == 'NOT-ILL'
        })  
    return (polished_data)

def scan_db():
    web_access = list(web_col.find())[0]
    if(len(web_access["queue"]) == 0):
        return {"empty": True}
    else:
        return {"empty":False, "token":web_access["queue"][0]}#FIFO

def add_queue(token):
    web_col.update_one(
        {"_id": ObjectId("60432bedbed23dfed0b5ddc7")},
        { "$push": { "queue": token } })
    return {
        "message": "success"
    }

def let_me(passy):
    return {
        "access": (passy == "koffmaster64")
    }

def poppy():
    web_col.update_one(
        {"_id": ObjectId("60432bedbed23dfed0b5ddc7")},
        {"$pop": { "queue": -1 } })
    return {"message":"success"}



if __name__ == "__main__":
    print(add_queue("604316fa8c5e79b3f3916802"))