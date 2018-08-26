from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users': 0
    
    })

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num+1
        UserNum.update({}, {"$set":{"num_of_users": new_num}})
        return str("Hello user: " + str(new_num))
    

def checkpostedData(postedData, functionName):
    if(functionName=="add" or functionName=="subtract" or functionName=="multiply" or functionName=="divide"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200

class Add(Resource):
    def post(self):
        #I have entered post to add operation
        
        #Step1: Get posted data
        postedData = request.get_json()
        
        #Step 1a: Check validity of posted data
        statusCode = checkpostedData(postedData, "add")
        if(statusCode!=200):
            retJson = {
                "Message": "An error occured",
                "Status Code": statusCode
                }
            return jsonify(retJson)
        
        #IF parameters are valid and status code is 200
        x = postedData["x"]
        y = postedData["y"]
        
        x=int(x)
        y=int(y)
        #Step 2: Add posted data
        ret = x+y
        
        #Step 3: return response
        retMap = {
            "Message": ret,
            "Status Code": 200

            }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        
        #Step1: Get posted Data
        postedData = request.get_json()
        
        #Check Validity of received data
        statusCode = checkpostedData(postedData, "subtract")
        if(statusCode!=200):
            retJson = {
                "Message": "An error occured",
                "Status Code": statusCode
                }
            return jsonify(retJson)
        
        #IF i am here get x and y from posted Data
        x = postedData["x"]
        y = postedData["y"]
        
        x = int(x)
        y = int(y)
        
        #Compute result
        ret = x-y
        
        retJson = {
            "Message": ret,
            "Status Code": 200
            }
        return jsonify(retJson)
        

class Multiply(Resource):
    def post(self):
        #First receive the posted data
        
        postedData = request.get_json()
        
        #Check validity of posted data
        statusCode = checkpostedData(postedData, "multiply")
        
        if(statusCode!=200):
            retJson = {
                "Message": "An error occured",
                "Status Code": statusCode
                }
            return jsonify(retJson)
        
        #Get data from posted data
        x = int(postedData["x"])
        y = int(postedData["y"])
        
        #Do multiply now
        ret = x*y
        
        retJson = {
            "Message": ret,
            "Status Code": statusCode
            }
        return jsonify(retJson)
        
    
class Divide(Resource):
    def post(self):
        
        #First recv posted data
        postedData = request.get_json()
        
        statusCode = checkpostedData(postedData, "divide")
        
        if(statusCode!=200):
            retJson = {
                "Message": "An error occured",
                "Status Code": statusCode
                }
            return jsonify(retJson)
        
        #Extract x and y
        x = int(postedData["x"])
        y = int(postedData["y"])
        
        if(y!=0):
            ret = x/y
            retJson = {
                "Message": ret,
                "Status Code": statusCode
                }
        else:
            retJson = {
                "Message": "Y cannot be 0..PLS!!, Invalid operation",
                "Status Code": 302
                }
        return jsonify(retJson)
    
    
#Init API using flask_Restfull api library
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
    return "Hello world"


if __name__ == "__main__":
    app.run(host='0.0.0.0')