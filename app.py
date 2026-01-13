from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('puntos.db')
    conn.execute('CREATE TABLE IF NOT EXISTS lista (name TEXT, score INTEGER)')
    return conn

# Esta ruta usa barras / para que Clickteam no se confunda
@app.route('/add/<nombre>/<puntos>')
def add(nombre, puntos):
    conn = get_db()
    conn.execute('INSERT INTO lista (name, score) VALUES (?, ?)', (nombre, puntos))
    conn.commit()
    conn.close()
    return "OK"

@app.route('/list')
def list_scores():
    conn = get_db()
    cursor = conn.execute('SELECT name, score FROM lista ORDER BY score DESC LIMIT 10')
    lineas = [f"{r[0]}:{r[1]}" for r in cursor.fetchall()]
    conn.close()
    return "|".join(lineas) if lineas else "Vacio"

@app.route('/clear')
def clear():
    conn = get_db()
    conn.execute('DELETE FROM lista')
    conn.commit()
    conn.close()
    return "Lista Vacia"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
