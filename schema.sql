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
CREATE TABLE training_sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users,
    last_accessed TIMESTAMP,
    vocab_hash TEXT,
    success_rate FLOAT
);

CREATE TABLE training_items(
    id INTEGER PRIMARY KEY,
    training_id INTEGER REFERENCES training_sessions,
    vocab_id INTEGER REFERENCES vocabs,
    success_rate FLOAT
);

CREATE TABLE vocab_categories(
    id INTEGER PRIMARY KEY,
    status_id INTEGER UNIQUE,
    status_description TEXT
);

