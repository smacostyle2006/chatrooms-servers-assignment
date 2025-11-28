DROP TABLE IF EXISTS users

CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    username    TEXT NOT NULL FOREIGN KEY,
    content     TEXT NOT NULL,
    date_sent   DATE NOT NULL,
    time_sent   TIME NOT NULL        
)