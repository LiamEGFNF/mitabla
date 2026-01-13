from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('puntos.db')
    # Definimos 'name' como PRIMARY KEY para que no se repita [cite: 2026-01-12]
    conn.execute('CREATE TABLE IF NOT EXISTS lista (name TEXT PRIMARY KEY, score INTEGER)')
    return conn

@app.route('/add/<nombre>/<puntos>')
def add(nombre, puntos):
    try:
        conn = get_db()
        puntos_nuevos = int(puntos)
        
        # Intentamos insertar. Si ya existe, fallará e irá al 'except' [cite: 2026-01-12]
        try:
            conn.execute('INSERT INTO lista (name, score) VALUES (?, ?)', (nombre, puntos_nuevos))
        except sqlite3.IntegrityError:
            # Si el nombre ya existe, verificamos si el puntaje es mejor [cite: 2026-01-12]
            cursor = conn.execute('SELECT score FROM lista WHERE name = ?', (nombre,))
            viejo_puntaje = cursor.fetchone()[0]
            if puntos_nuevos > viejo_puntaje:
                conn.execute('UPDATE lista SET score = ? WHERE name = ?', (puntos_nuevos, nombre))
        
        conn.commit()
        conn.close()
        return "OK"
    except Exception as e:
        return f"Error: {str(e)}"

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
    conn.execute('DROP TABLE IF EXISTS lista') # Borra todo para reiniciar con la nueva estructura
    conn.commit()
    conn.close()
    return "Lista Reiniciada"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
