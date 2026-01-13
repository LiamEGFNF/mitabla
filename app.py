from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/add')
def add():
    name = request.args.get('name')
    score = request.args.get('score')
    conn = sqlite3.connect('puntos.db')
    conn.execute('CREATE TABLE IF NOT EXISTS lista (name TEXT, score INTEGER)')
    conn.execute('INSERT INTO lista (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    return "OK"

@app.route('/list')
def list():
    conn = sqlite3.connect('puntos.db')
    cursor = conn.execute('SELECT name, score FROM lista ORDER BY score DESC LIMIT 10')
    return "|".join([f"{r[0]}:{r[1]}" for r in cursor.fetchall()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
