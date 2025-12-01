from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine("sqlite:///chatroom.db", echo=False)

@app.route("/signup", methods = ["GET", "POST"])
def create_user():
    if request.method == "POST":
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        abort(400, description = "Username and password required")

    

   
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        
if __name__ == "__main__":
    app.run(debug = True)