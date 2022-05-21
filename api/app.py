from flask import Flask, request, json, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def fetch_todos():
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        loaded_json_file.close()
        loaded_data.pop("index")
        return jsonify(loaded_data), 200
    except:
        return jsonify(error="Unable to fetch todos"), 500


@app.route("/index", methods=['GET'])
def fetch_index():
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        loaded_json_file.close()
        return jsonify(loaded_data["index"]), 200
    except:
        return jsonify(error="Unable to fetch index"), 500


@app.route("/index/update/<index>", methods=['PUT'])
def update_index(index):
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        index = request.arg.get("index")
        loaded_data["index"] = index
        loaded_json_file.write(json.dumps(loaded_data))
        loaded_json_file.close()
        return jsonify(message="Index updated successfully"), 201
    except:
        return jsonify(error="Unable to fetch index"), 500


@app.route("/create/<todo>", methods=['POST'])
def create_todo(todo):
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        todo = request.arg.get("todo")
        index = loaded_data["index"]
        loaded_data[str(index)] = todo
        loaded_json_file.write(json.dumps(loaded_data))
        loaded_json_file.close()
        return jsonify(message="Todo created successfully"), 201
    except:
        return jsonify(error="Todo not created"), 500


@app.route("/update/<todo>", methods=['PUT'])
def update_todo(todo):
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        todo = request.arg.get("todo")
        for i in loaded_data:
            if loaded_data[str(i)].index == todo.index:
                loaded_data[str(i)] = todo
        loaded_json_file.write(json.dumps(loaded_data))
        loaded_json_file.close()
        return jsonify(message="Todo updated successfully"), 201
    except:
        return jsonify(error="Todo not updated"), 500


@app.route("/delete/<todo>", methods=['DELETE'])
def delete_todo(todo):
    try:
        loaded_json_file = open('db.json')
        loaded_data = json.load(loaded_json_file)
        todo = request.arg.get("todo")
        for i in loaded_data:
            if loaded_data[str(i)].index == todo.index:
                loaded_data.pop(str(i))
        loaded_json_file.write(json.dumps(loaded_data))
        loaded_json_file.close()
        return jsonify(message="Todo deleted successfully"), 204
    except:
        return jsonify(error="Todo not deleted"), 500


@app.errorhandler(404)
def method_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == "__main__":
    app.run()
