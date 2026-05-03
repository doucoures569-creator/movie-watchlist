from flask import Flask, g
import sqlite3

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

@app.route('/')
def index():
    return "The Movie Watchlist application is ready!"

if __name__ == '__main__':
    app.run(debug=True)