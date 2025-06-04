from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import os
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(2000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))


    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/show")
def list():
    alltodo=Todo.query.all()
    print(alltodo)
    return 'this is todo list page'

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        title=(request.form['title'])
        desc=(request.form['desc'])
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/templates")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)



@app.route("/delete/<int:sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/templates")

@app.route("/templates",methods=['GET','POST']) # this is how we can make routs and  add more pages using function andby providing proper path
def products():
    if request.method=="POST":
        title=(request.form['title'])
        desc=(request.form['desc'])
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit() # will comit the changes
    alltodo=Todo.query.all()
    print(alltodo)
    return render_template('index.html',alltodo=alltodo)
if __name__ == "__main__":
    app.run(debug=True)