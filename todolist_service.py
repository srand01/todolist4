# Start of todolist_service.py

from flask import Flask, jsonify, request, g
import sqlite3

DATABASE = 'todolist.db'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/api/items", methods=['GET'])
def get_items():
    db = get_db()
    cur = db.execute('SELECT what_to_do, due_date, status FROM entries')
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2]) for row in entries]
    return jsonify(tdlist)

@app.route("/api/items", methods=['POST'])
def add_item():
    db = get_db()
    db.execute('insert into entries (what_to_do, due_date) values (?, ?)',
               [request.json['what_to_do'], request.json['due_date']])
    db.commit()
    return jsonify({'status': 'success'})

@app.route("/api/items/<item>", methods=['DELETE'])
def delete_item(item):
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({'status': 'success'})

@app.route("/api/items/<item>", methods=['PUT'])
def mark_item(item):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({'status': 'success'})

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)
# End of todolist_service.py
