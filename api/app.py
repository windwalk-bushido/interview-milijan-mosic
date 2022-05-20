from flask import Flask, json

app = Flask(__name__)


@app.route("/")
def fetch_todos():
    loaded_json_file = open('db.json')
    load_db = json.load(loaded_json_file)
    loaded_json_file.close()
    return load_db, 200


if __name__ == "__main__":
    app.run()
