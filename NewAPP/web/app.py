""" 
Registration of user (0 tokens - free)
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on our database for 1 token
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")

db = client.SentencesDatabase
#Collections
users = db["Users"]

class Register(Resource):
    def post(self):
        #Step 1: get posted data by user
        postedData = request.get_json()
        
        #Get the data from postedData
        username = postedData["username"]
        password = postedData["password"]
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        
        #Store username and password into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
            })
        
        retJson = {
            "status": 200,
            "msg": "Successfully signed up for the API"
            
            }
        
        return jsonify(retJson)

#helper functions for Store
def verifyPW(username, password):
    hashed_pw = users.find({
            "Username": username
        })[0]["Password"]
        
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:        
        return False
        
def countTokens(username):
    tokens = users.find({
        "Username": username
        })[0]["Tokens"]
        
    return tokens

#Ends here

class Store(Resource):
    def post(self):
        
        postedData = request.get_json()
        
        #REad the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        
        #Step 3: verify username and password matches with registered
        correct_pw = verifyPW(username, password)
        
        if not correct_pw:
            retJson = {
                "status": 302,
                "Message": "Password incorrect"
                }
            return jsonify(retJson)
        
        #Step4: Verify he has enough tokens
        num_tokens = countTokens(username)
        
        if num_tokens<=0:
            retJson = {
                "status": 301,
                "Message": "Out of tokens"
                }
        
        #Step 5: Store sentence and take away 1 token and return 200 OK
        users.update({
            "Username": username            
            }, {
                "$set": {
                    "Sentence": sentence,
                    "Tokens": num_tokens-1
                    }
                })
        
        retJson = {
            "status": 200,
            "msg": "Sentence saved successfully"
            }
        
        return jsonify(retJson)
        
class Get(Resource):
    def post(self):
        
        postedData = request.get_json()
        
        #Get data
        username = postedData["username"]
        password = postedData["password"]
        
        #Step 3: verify username and password matches with registered
        correct_pw = verifyPW(username, password)
        
        if not correct_pw:
            retJson = {
                "status": 302,
                "Message": "Password incorrect"
                }
            return jsonify(retJson)
        
        #Step4: Verify he has enough tokens
        num_tokens = countTokens(username)
        
        if num_tokens<=0:
            retJson = {
                "status": 301,
                "Message": "Out of tokens"
                }
            return jsonify(retJson)
        
        #MAke user pay - take away 1 token everytime
        users.update({
            "Username": username            
            }, {
                "$set": {
                    "Tokens": num_tokens-1
                    }
                })
        
        
        
        sentence = users.find({
            "Username": username
            })[0]["Sentence"]
            
        retJson = {
            "status": 200,
            "Sentence": sentence
            }
        
        return jsonify(retJson)
            








api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')



if __name__=="__main__":
    app.run(host='0.0.0.0')
    






"""
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


"""