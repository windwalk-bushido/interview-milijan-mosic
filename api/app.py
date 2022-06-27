from flask import Flask, request, json
from flask_restful import Resource, Api
from flask_cors import CORS
from os import environ, urandom
from datetime import datetime
from passlib.hash import pbkdf2_sha256
import uuid


app = Flask(__name__)
CORS(app)
api = Api(app)


class Wiki(Resource):
    def get(self):
        helper = dict()
        helper.update(
            {"welcome": "Hello, you're at the root of the Flask app'"})
        helper.update({"todos": "Fetch todos by heading to '/todos'"})
        helper.update({"index": "Fetch index by heading to '/index'"})
        helper.update({"message": "Thanks!'"})
        return helper, 200


class User:
    def __init__(self, index, username, uuid, password, date_created):
        self.index = index
        self.username = username
        self.uuid = str(uuid)
        self.password = password
        self.date_created = str(date_created)
        self.date_modified = ""


class Todo:
    def __init__(self, index, belongs_to, body, done, date_created):
        self.index = index
        self.belongs_to = belongs_to
        self.body = body
        self.done = done
        self.date_created = str(date_created)
        self.date_modified = ""


def DoesRequestHaveAPIKey(key):
    if(key == environ.get('API_KEY')):
        return True
    else:
        return False


def LoadData():
    with open("db.json", "rt", encoding="utf-8") as file:
        wanted_data = json.load(file)
        return wanted_data


def SaveData(data):
    with open("db.json", "wt", encoding="utf-8") as file:
        data_to_write = json.dumps(
            data, indent=2, sort_keys=True)
        file.write(data_to_write)


class Login(Resource):
    def post(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                wanted_data = loaded_data["users"]
                for i in wanted_data:
                    user = wanted_data.get(i)
                    if user["username"] == arrived_data["username"]:
                        if pbkdf2_sha256.verify(
                                arrived_data["password"], user["password"]):
                            return {"message": "Login successfull", "uuid": user["uuid"]}, 200
            except:
                return {"error": "Credentials are wrong."}, 500
        else:
            return {"error": "API key is wrong."}, 500


class Register(Resource):
    def post(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                wanted_data = loaded_data["users"]
                if len(wanted_data.keys()) >= 2:
                    for i in wanted_data:
                        user = wanted_data.get(i)
                        if user["username"] == arrived_data["username"]:
                            print("Username already exists.")
                            return {"error": "Username already exists."}, 500
                index = wanted_data["index"]
                hashed_password = pbkdf2_sha256.hash(
                    arrived_data["password"])
                new_user = User(index, arrived_data["username"], uuid.uuid4(
                ), hashed_password, datetime.utcnow())
                wanted_data.update({str(index): new_user.__dict__})
                index += 1
                wanted_data["index"] = index
                loaded_data["users"] = wanted_data
                SaveData(loaded_data)
                return {"message": "Register successfull", "uuid": new_user.uuid}, 201
            except:
                return {"error": "Something is wrong."}, 500
        else:
            return {"error": "API key is wrong."}, 500


class Todos(Resource):
    def get(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                loaded_data.pop("index")
                return loaded_data, 200
            except:
                return {"error": "Unable to fetch todos"}, 500
        else:
            return {"error": "API key is wrong."}, 500

    def post(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                index = loaded_data["index"]
                loaded_data.update({str(index): arrived_data["todo"]})
                SaveData(loaded_data)
                return {"message": "Todo created successfully"}, 201
            except:
                return {"error": "Todo not created"}, 500
        else:
            return {"error": "API key is wrong."}, 500

    def put(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            loaded_data = LoadData()
            if arrived_data["mode"] == "put":
                try:
                    for i in loaded_data:
                        todo = loaded_data.get(i)
                        if todo["index"] == arrived_data["todo"]["index"]:
                            loaded_data.update({str(i): arrived_data["todo"]})
                            SaveData(loaded_data)
                            return {"message": "Todo updated successfully"}, 200
                except:
                    return {"error": "Todo not updated"}, 500
            if arrived_data["mode"] == "delete":
                try:
                    index_for_deletion = arrived_data["target"]
                    for i in loaded_data:
                        todo = loaded_data.get(i)
                        if todo["index"] == int(index_for_deletion):
                            loaded_data.pop(str(i))
                            SaveData(loaded_data)
                            return {"message": "Todo deleted successfully"}, 200
                except:
                    return {"error": "Todo not deleted"}, 500
        else:
            return {"error": "API key is wrong."}, 500


class Index(Resource):
    def get(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                return loaded_data["index"], 200
            except:
                return {"error": "Unable to fetch index"}, 500
        else:
            return {"error": "API key is wrong."}, 500

    def put(self):
        arrived_data = request.get_json()
        if DoesRequestHaveAPIKey(arrived_data["API_KEY"]):
            try:
                loaded_data = LoadData()
                loaded_data["index"] = arrived_data["index"]
                SaveData(loaded_data)
                return {"message": "Index updated successfully"}, 200
            except:
                return {"error": "Unable to fetch index"}, 500
        else:
            return {"error": "API key is wrong."}, 500


@app.errorhandler(404)
def method_not_found(e):
    return {"error": str(e)}, 404


api.add_resource(Wiki, "/")
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Todos, "/todos")
api.add_resource(Index, "/index")


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
