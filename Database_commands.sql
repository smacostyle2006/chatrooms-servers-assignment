/*This file is only for pre-type sql commands to have IDE help with auto-typing instead of typing in string in python*/
DROP TABLE IF EXISTS users

CREATE TABLE users (
    id          INTEGER PRIMARY KEY,
    username    TEXT NOT NULL FOREIGN KEY,
    content     TEXT NOT NULL,
    date_sent   DATE NOT NULL,
    time_sent   TIME NOT NULL       
    username    TEXT NOT NULL FOREIGN KEY REFERENCES users(username), 
)