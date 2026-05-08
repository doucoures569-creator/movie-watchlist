# app.py
from flask import Flask, g, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from logic import is_valid_title, is_valid_rating

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username or not password:
            error = 'Username and password are required.'
        else:
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."

        if error:
            flash(error)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form['title']
        if is_valid_title(title):
            db.execute('INSERT INTO movies (user_id, title) VALUES (?, ?)', (user_id, title.strip()))
            db.commit()
        return redirect(url_for('index'))

    filter_status = request.args.get('filter')
    if filter_status in ['Watched', 'To Watch']:
        cursor = db.execute('SELECT * FROM movies WHERE user_id = ? AND status = ?', (user_id, filter_status))
    else:
        cursor = db.execute('SELECT * FROM movies WHERE user_id = ?', (user_id,))
        
    movies = cursor.fetchall()
    return render_template('index.html', movies=movies, current_filter=filter_status)

@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM movies WHERE id = ? AND user_id = ?', (movie_id, session['user_id']))
    db.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:movie_id>', methods=['POST'])
def toggle_status(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    movie = db.execute('SELECT status FROM movies WHERE id = ? AND user_id = ?', (movie_id, session['user_id'])).fetchone()
    if movie:
        new_status = 'Watched' if movie['status'] == 'To Watch' else 'To Watch'
        db.execute('UPDATE movies SET status = ? WHERE id = ?', (new_status, movie_id))
        db.commit()
    return redirect(url_for('index'))

@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    rating = request.form.get('rating')
    if is_valid_rating(rating):
        db = get_db()
        db.execute('UPDATE movies SET rating = ? WHERE id = ? AND user_id = ?', (int(rating), movie_id, session['user_id']))
        db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)