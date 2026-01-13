from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('puntos.db')
    # Creamos la tabla si no existe [cite: 2026-01-12]
    conn.execute('CREATE TABLE IF NOT EXISTS lista (name TEXT PRIMARY KEY, score INTEGER)')
    return conn

@app.route('/add/<nombre>/<puntos>')
def add(nombre, puntos):
    conn = get_db()
    # Buscamos si el jugador ya está en el cuaderno [cite: 2026-01-12]
    cursor = conn.execute('SELECT score FROM lista WHERE name = ?', (nombre,))
    fila = cursor.fetchone()
    
    puntos_nuevos = int(puntos)
    
    if fila:
        # Si ya existe, solo actualizamos si el puntaje nuevo es mejor [cite: 2026-01-12]
        if puntos_nuevos > fila[0]:
            conn.execute('UPDATE lista SET score = ? WHERE name = ?', (puntos_nuevos, nombre))
    else:
        # Si es nuevo, lo registramos normal [cite: 2026-01-12]
        conn.execute('INSERT INTO lista (name, score) VALUES (?, ?)', (nombre, puntos_nuevos))
        
    conn.commit()
    conn.close()
    return "OK"

@app.route('/list')
def list_scores():
    conn = get_db()
    # Traemos los mejores 10 ordenados por puntaje [cite: 2026-01-12]
    cursor = conn.execute('SELECT name, score FROM lista ORDER BY score DESC LIMIT 10')
    lineas = [f"{r[0]}:{r[1]}" for r in cursor.fetchall()]
    conn.close()
    # Si la lista está vacía, devuelve "Vacio" [cite: 2026-01-12]
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
