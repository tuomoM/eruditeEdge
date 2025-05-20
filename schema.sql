CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE vocabs(
    id INTEGER PRIMARY KEY,
    global_flag INTEGER,
    word TEXT,
    w_description TEXT,
    example TEXT,
    synonyms TEXT,
    user_id INTEGER REFERENCES users

);

