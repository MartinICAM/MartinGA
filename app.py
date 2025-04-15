from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)
DB_FILE = 'cartons.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cartons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            couleur TEXT NOT NULL,
            date_heure TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nouveau')
def nouveau_carton():
    return render_template('nouveau.html')

@app.route('/valider', methods=['POST'])
def valider():
    couleur = request.form.get('couleur')
    date_heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO cartons (couleur, date_heure) VALUES (?, ?)', (couleur, date_heure))
    conn.commit()
    conn.close()

    return redirect(url_for('liste'))

@app.route('/liste')
def liste():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT couleur, date_heure FROM cartons ORDER BY id DESC')
    cartons = c.fetchall()
    conn.close()
    return render_template('liste.html', cartons=cartons)

# Ajoute ce bloc pour rendre l'app compatible avec Vercel en tant que fonction serverless
if __name__ == "__main__":
    app.run(debug=True)

