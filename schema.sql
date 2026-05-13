DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS movies;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'To Watch',
    rating INTEGER DEFAULT 0,
    watched_at DATETIME,
    review TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);