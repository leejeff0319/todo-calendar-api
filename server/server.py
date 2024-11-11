from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# app instance
app = Flask(__name__)
app.config('SQLALCHEMY_DATABASE_URL')='sqlite:///db.sqlite'
app.config('SQLALCHEMY_TRACK_MODIFICATIONS')=False
db = SQLAlchemy(app)

CORS(app)

class Todo(db.Model):
    # userid = db.Colum(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)

# /api/home
@app.route('/api/home', methods=["GET"])
def home():
    todo_list=Todo.query.all()
    return jsonify({
        'todo_list': todo_list,
    })

@app.route('/add', methods=['POST'])
def add():
    name=request.form.get("name")
    new_task = Todo(name=name, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8080)                     # remove debug in deployment
    