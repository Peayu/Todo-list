from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(2000), nullable = False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    completed = db.Column(db.Boolean, default =False)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST" :
        title = request.form["title"]
        desc = request.form["desc"]
        if title & desc:
            todo = Todo(title=title, desc =desc)
            db.session.add(todo)
            db.session.commit()

    allTodo = Todo.query.order_by(Todo.date_created.desc()).all()

    return render_template('index.html', allTodo = allTodo)


@app.route('/complete/<int:sno>')
def complete(sno):

    todo = Todo.query.filter_by(sno=sno).first()

    todo.completed = True

    db.session.commit()

    return redirect('/')

@app.route('/deletee/<int:sno>')
def deletee(sno):

    todo = Todo.query.filter_by(sno=sno).first()


    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)