from flask import Flask, jsonify, request, redirect, url_for, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

# app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key for JWT
db = SQLAlchemy(app)
CORS(app)

# Define the User and Todo models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Todo(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date)  
    task_id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)

# /api/home (retrieve all todos for a user)
@app.route('/api/home', methods=["GET"])
def home():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
            todo_list = Todo.query.filter_by(user_id=user_id).all()
            todos = [{'task_id': todo.task_id, 'name': todo.name, 'done': todo.done} for todo in todo_list]
            return jsonify({'todo_list': todos})
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired, log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token, please log in.'}), 401
    return jsonify({'error': 'Authorization token required.'}), 403

# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

# User Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid credentials.'}), 401

# Todo Routes: Add, Update, Delete
@app.route('/add', methods=['POST'])
def add():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        name = request.json.get("name")
        new_task = Todo(name=name, user_id=user_id, done=False)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully.'}), 201
    return jsonify({'error': 'Authorization token required.'}), 403

@app.route('/update/<int:todo_id>', methods=['POST'])
def update(todo_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        
        todo = Todo.query.filter_by(task_id=todo_id, user_id=user_id).first()
        if todo:
            todo.done = not todo.done
            db.session.commit()
            return jsonify({'message': 'Task updated successfully.'})
        return jsonify({'error': 'Task not found.'}), 404
    return jsonify({'error': 'Authorization token required.'}), 403

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete(todo_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        
        todo = Todo.query.filter_by(task_id=todo_id, user_id=user_id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully.'})
        return jsonify({'error': 'Task not found.'}), 404
    return jsonify({'error': 'Authorization token required.'}), 403

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8080)  # remove debug in deployment
