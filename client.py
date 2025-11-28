from sqlalchemy import create_engine

engine = create_engine("sqlite:///chatroom.db", echo=False)

with engine.begin() as conn:
    conn.exec_driver_sql("DROP TABLE IF EXISTS users")