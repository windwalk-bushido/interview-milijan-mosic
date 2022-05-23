from flask import Flask, request, json
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)


class Todos(Resource):
    def get(self):
        try:
            loaded_json_file = open("db.json", "rt")
            loaded_data = json.load(loaded_json_file)
            loaded_json_file.close()
            loaded_data.pop("index")
            return loaded_data, 200
        except:
            return {"error": "Unable to fetch todos"}, 500

    def post(self):
        try:
            loaded_json_file = open("db.json", "rt")
            loaded_data = json.load(loaded_json_file)
            arrived_data = request.get_json()
            index = loaded_data["index"]
            loaded_data.update({str(index): arrived_data["todo"]})
            with open("db.json", "wt", encoding="utf-8") as file:
                data_to_write = json.dumps(
                    loaded_data, indent=2, sort_keys=True)
                file.write(data_to_write)
            return {"message": "Todo created successfully"}, 201
        except:
            return {"error": "Todo not created"}, 500

    def put(self):
        loaded_json_file = open("db.json", "rt")
        loaded_data = json.load(loaded_json_file)
        arrived_data = request.get_json()
        print(arrived_data)
        if arrived_data["mode"] == "put":
            try:
                for i in loaded_data:
                    todo = loaded_data.get(i)
                    if todo["index"] == arrived_data["todo"]["index"]:
                        loaded_data.update({str(i): arrived_data["todo"]})
                        with open("db.json", "wt", encoding="utf-8") as file:
                            data_to_write = json.dumps(
                                loaded_data, indent=2, sort_keys=True)
                            file.write(data_to_write)
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
                        with open("db.json", "wt", encoding="utf-8") as file:
                            data_to_write = json.dumps(
                                loaded_data, indent=2, sort_keys=True)
                            file.write(data_to_write)
                            return {"message": "Todo deleted successfully"}, 200
            except:
                return {"error": "Todo not deleted"}, 500


class Index(Resource):
    def get(self):
        try:
            loaded_json_file = open("db.json", "rt")
            loaded_data = json.load(loaded_json_file)
            loaded_json_file.close()
            return loaded_data["index"], 200
        except:
            return {"error": "Unable to fetch index"}, 500

    def put(self):
        try:
            loaded_json_file = open("db.json", "rt")
            loaded_data = json.load(loaded_json_file)
            arrived_data = request.get_json()
            loaded_data["index"] = arrived_data["index"]
            with open("db.json", "wt", encoding="utf-8") as file:
                data_to_write = json.dumps(
                    loaded_data, indent=2, sort_keys=True)
                file.write(data_to_write)
            return {"message": "Index updated successfully"}, 200
        except:
            return {"error": "Unable to fetch index"}, 500


@app.errorhandler(404)
def method_not_found(e):
    return {"error": str(e)}, 404


api.add_resource(Todos, "/todos", methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(Index, "/index", methods=['GET', 'PUT'])


if __name__ == "__main__":
    app.run()
