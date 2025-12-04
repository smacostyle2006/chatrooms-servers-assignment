from sqlalchemy import create_engine

engine = create_engine("sqlite:///chatroom.db", echo=False)

with engine.begin() as conn:
   conn.exec_driver_sql("Drop table users")
   conn.exec_driver_sql("DROP table messages")

with engine.begin() as conn:

    conn.exec_driver_sql("""
        CREATE TABLE users (
            id          INTEGER PRIMARY KEY,
            username    TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL
        )
    """)
    conn.exec_driver_sql("""
        CREATE TABLE messages (
            id          INTEGER PRIMARY KEY,
            username    TEXT NOT NULL REFERENCES users(username),
            content     TEXT NOT NULL,
            date_sent   DATE NOT NULL,
            time_sent   TIME NOT NULL
        )
    """)



