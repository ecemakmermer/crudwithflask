from flask import Flask,Response,request
import pymongo
import json
from bson.objectid import ObjectId
app=Flask(__name__)

try:
    mongo= pymongo.MongoClient(
        host="localhost", 
        port=27017,
        serverSelectionTimeoutMS= 1000
        )
    db = mongo.school
    mongo.server_info()
except:
    print("ERROR cannot connect to db")

###########################
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user={"name":request.form["name"],"lastName": request.form["lastName"],"studentNo": request.form["studentNo"]}
        resp=db.users.insert_one(user)
        print(resp.inserted_id)
        
        return Response(
            response=json.dumps({"message":"user created","id":f"{resp.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(Exception)
        return Response(
            response=json.dumps({"message":"cannot create user"}),
            status=500,
            mimetype="application/json"
        )
##########################
@app.route("/users",methods=["GET"])
def read_users():
    try:
        data= list(db.users.find())
        for user in data:
            user["_id"]= str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json")

    except:
        print(Exception)
        return Response(
            response=json.dumps({"message":"cannot read users"}),
            status=200,
            mimetype="application/json")
###########################
@app.route("/users/<id>", methods=["PATCH"])
def update_users(id):
    try:
        resp = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        if resp.modified_count ==1:
            return Response(
                response=json.dumps({"message":"user updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message":"no update"}),
                status=200,
                mimetype="application/json"
            )


    except:
        print(Exception)
        return Response(
            response=json.dumps({"message":"cannot update user"}),
            status=500,
            mimetype="application/json"
        )


###########################
@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        resp = db.users.delete_one({"_id":ObjectId(id)})
        if resp.deleted_count==1:
            return Response(
                response=json.dumps({"message":"user deleted","id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
    except:
        print(Exception)
        return Response(
            response=json.dumps({"message":"cannot delete user"}),
            status=500,
            mimetype="application/json"
        )

###########################
if __name__=="__main__":
    app.run(port=80,debug=True)
