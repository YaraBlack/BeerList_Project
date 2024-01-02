from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import readconfig


app = Flask(__name__)

config = readconfig.readConfig()
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config["BD_USER"]}:\
{config["BD_PASSWORD"]}@localhost:5432/users_db"

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(20), nullable=False)

@app.route("/register", methods=['POST'])
def register_user():
    data = request.get_json(force=False, silent=False, cache=False)
    username = data.get('username')
    password = data.get('password')
    
    newUser = User(username=username, password_hash=password)
    with app.app_context():
        db.session.add(newUser)
        db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 200

@app.route("/login", methods=['POST'])
def auth():
    data = request.get_json(force=False, silent=False, cache=False)
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, password_hash=password).first()
    
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

def start():
    app.run(debug=True, port=5001)
    
start()