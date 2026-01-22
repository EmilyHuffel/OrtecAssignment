from flask import Flask, render_template, request, flash
from task_list import TaskList
import sys 

app = Flask(__name__)
app.secret_key = "super_secret_passkey"

tasks = TaskList(sys.stdin, sys.stdout)

@app.route("/tasks")
def welcome():
	flash("Welcome to TaskList! Type 'help' for available commands.\n")
	return render_template("tasks.html")

@app.route("/tasks", methods=['POST', 'GET'])
def response():
	flash(tasks.execute(str(request.form['command_input'])))
	return render_template("tasks.html")

@app.route("/projects", methods=["GET"])
def projects():
	flash(tasks.execute('show'))
	return render_template('projects.html')

@app.route("/projects", methods=["POST", "GET"])
def add_projects():
    tasks.execute(f"add project {request.form['project_to_create']}")
    flash(tasks.execute('show').replace("\n", '<br>'))
    return render_template('projects.html')