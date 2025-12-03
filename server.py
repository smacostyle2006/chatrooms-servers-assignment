from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)
engine = create_engine("sqlite:///chatroom.db", echo=False)

# ------------------ SIGNUP ------------------
@app.route("/signup", methods=["POST"])
def signup():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        abort(400, description="Username and password required")
     
    with engine.begin() as conn:
        try:
            conn.execute(
                text("INSERT INTO users (username, password) VALUES (:u, :p)"),
                {"u": username, "p": password}
            )
        except:
            abort(401, description="Username already taken")

    return jsonify({"message": "User created"}), 201
    

# ------------------ LOGIN ------------------ 
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        with engine.begin() as conn:
           row = conn.execute(
            text("SELECT * FROM users WHERE username = :u AND password = :p"),
            {"u": username, "p": password}
        ).fetchone()

        if row is None:
         abort(401, description="Invalid username or password")

    return jsonify({"message": "Login successful"})

# ------------------ SEND MESSAGE ------------------
@app.route("/send", methods=["POST"])
def send_message():

    username = request.form.get("username", "").strip()
    content  = request.form.get("content", "").strip()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO messages (username, content, date_sent, time_sent)
                VALUES (:u, :c, :d, :t)
            """),
            {"u": username, "c": content, "d": date, "t": time}
        )

    return jsonify({"message": "Message stored"})

# ------------------ GET MESSAGES ------------------
@app.route("/messages", methods=["GET"])
def messages():
    
    last_id = request.args.get("last_id", 0)

    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                 SELECT id, username, content, date_sent, time_sent 
                 FROM messages
                 WHERE id > :last_id
                 ORDER BY id ASC
                 """), {"last_id":last_id}
        ).fetchall()

    output = []
    for r in rows:
        output.append({
            "id":       r[0],
            "username": r[1],
            "content":  r[2],
            "date":     r[3],
            "time":     r[4]
        })

    return jsonify({"messages": output})

        
if __name__ == "__main__":
    app.run(port=65435, debug=True)