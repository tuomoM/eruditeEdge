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
    session_description TEXT,
    user_id INTEGER REFERENCES users,
    last_accessed TIMESTAMP,
    vocab_hash TEXT,
    success_rate FLOAT
);

CREATE TABLE training_items(
    id INTEGER PRIMARY KEY,
    training_id INTEGER REFERENCES training_sessions,
    vocab_id INTEGER REFERENCES vocabs
);

CREATE TABLE status_categories(
    id INTEGER PRIMARY KEY,
    category_type TEXT,
    status_id INTEGER UNIQUE,
    status_description TEXT
);
CREATE TABLE change_suggestions(
    id INTEGER PRIMARY KEY,
    owner_id INTEGER REFERENCES users,
    vocab_id INTEGER REFERENCES vocabs,
    creator_id INTEGER REFERENCES users,
    new_description TEXT,
    new_example TEXT,
    new_synonyms TEXT,
    change_status INTEGER REFERENCES status_categories,
    creation_time TIMESTAMP,
    comments TEXT
);
CREATE TABLE vocab_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id),
    vocab_id INTEGER REFERENCES vocabs(id),
    last_success_status INTEGER REFERENCES status_categories(status_id),
    last_updated TIMESTAMP,
    UNIQUE (user_id, vocab_id)
);

