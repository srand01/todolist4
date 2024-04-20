# Start of todolist.py

# This is a simple example web app that is meant to illustrate the basics.
from flask import Flask, render_template, redirect, request, url_for, jsonify
import sqlite3
import requests

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def show_list():
    resp = requests.get("http://localhost:5001/api/items")
    resp = resp.json()
    return render_template('index.html', todolist=resp)

@app.route("/add", methods=['POST'])
def add_entry():
    data = {
        'what_to_do': request.form['what_to_do'],
        'due_date': request.form['due_date']
    }
    requests.post("http://localhost:5001/api/items", json=data)
    return redirect(url_for('show_list'))

@app.route("/delete/<item>")
def delete_entry(item):
    requests.delete(f"http://localhost:5001/api/items/{item}")
    return redirect(url_for('show_list'))

@app.route("/mark/<item>")
def mark_as_done(item):
    requests.put(f"http://localhost:5001/api/items/{item}")
    return redirect(url_for('show_list'))

if __name__ == "__main__":
    app.run("0.0.0.0")
    
# End of todolist.py
