from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, text
from datetime import datetime

app = Flask(__name__)
engine = create_engine("sqlite:///chatroom.db", echo=False)

#-------------password Encoding--------------
def encode_password(password):
    return password[::-1]         # Store reversed password
 
def check_password(plain):
    return plain[::-1]         #Compare reversed versions

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
                {"u": username, "p": encode_password(password)}
            )
        except:
            abort(409, description="Username already exists")
 
    return jsonify({"message": "User created"}), 201
    

# ------------------ LOGIN ------------------
@app.route("/login", methods = ["POST"])
def login():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        with engine.begin() as conn:
           row = conn.execute(
            text("SELECT * FROM users WHERE username = :u AND password = :p"),
            {"u": username, "p": check_password(password)}
        ).fetchone()

        if row is None:
         abort(401, description="Invalid username or password")

        return jsonify({"message": "Login successful"}), 200

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

    return jsonify({"message": "Message stored"}), 201

# ------------------ GET MESSAGES ------------------
@app.route("/messages", methods=["GET"])
def messages():
    
    with engine.begin() as conn:
        rows = conn.execute(
            text("""
                 SELECT username, content, date_sent, time_sent 
                 FROM messages
                 """)
        ).fetchall()

    output = []
    for r in rows:
        output.append({
            "username": r[0],
            "content":  r[1],
            "date":     r[2],
            "time":     r[3]
        })

    return jsonify({"messages": output})

        
if __name__ == "__main__":
    app.run(port=65435, debug=True) 