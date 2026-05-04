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
            db.execute('INSERT INTO movies (user_id, title) VALUES (?, ?)', (1, title))
            db.commit()
        return redirect(url_for('index'))
        
    cursor = db.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    return render_template('index.html', movies=movies)

@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    db = get_db()
    db.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>', methods=['POST'])
def toggle_status(movie_id):
    db = get_db()
    movie = db.execute('SELECT status FROM movies WHERE id = ?', (movie_id,)).fetchone()
    if movie:
        new_status = 'Watched' if movie['status'] == 'To Watch' else 'To Watch'
        db.execute('UPDATE movies SET status = ? WHERE id = ?', (new_status, movie_id))
        db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)