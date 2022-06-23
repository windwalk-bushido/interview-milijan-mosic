from flask import Flask, request, json
from flask_restful import Resource, Api
from flask_cors import CORS
from os import environ
import models

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


def DoesRequestHaveAPIKey(key):
    if(key == environ.get('API_KEY')):
        return True
    else:
        return False


def LoadData():
    loaded_json_file = open("db.json", "rt")
    wanted_data = json.load(loaded_json_file)
    loaded_json_file.close()
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
                return {"message": "Login successfull", "id": "0001"}, 201
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
api.add_resource(Todos, "/todos")
api.add_resource(Index, "/index")


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
