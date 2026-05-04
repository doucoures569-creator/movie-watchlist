-- schema.sql
DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'To Watch',
    rating INTEGER DEFAULT 0
);