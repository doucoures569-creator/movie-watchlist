from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions'
DATABASE = 'database.sqlite3'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if not os.path.exists(DATABASE):
    init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        if title:
            # Note: We temporarily hardcode user_id 1 until user authentication is added
            db.execute('INSERT INTO movies (user_id, title) VALUES (?, ?)', (1, title))
            db.commit()
        return redirect(url_for('index'))
        
    cursor = db.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)