from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(["Task 1", "Task 2", "Task 3"])
