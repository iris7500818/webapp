from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import os
from datetime import datetime


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


app.config["SECRET_KEY"] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    contents = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def set_login_user_name():
    global login_user_name
    login_user_name = current_user.username if current_user.is_authenticated else None


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    search_word = request.args.get("search_word")

    if search_word is None:
        message_list = Message.query.all()
    else:
        message_list = Message.query.filter(
            Message.contents.like(f"%{search_word}%")
        ).all()

    return render_template(
        "top.html",
        login_user_name=login_user_name,
        message_list=message_list,
        search_word=search_word,
    )


@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template("write.html", login_user_name=login_user_name)
    elif request.method == "POST":
        contents = request.form.get("contents")
        user_name = request.form.get("user_name")
        new_message = Message(user_name=user_name, contents=contents)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/update/<int:message_id>", methods=["GET", "POST"])
def update(message_id):
    message = Message.query.get(message_id)

    if request.method == "GET":
        return render_template(
            "update.html", login_user_name=login_user_name, message=message
        )
    elif request.method == "POST":
        message.contents = request.form.get("contents")
        db.session.commit()

        return redirect(url_for("index"))


@app.route("/delete/<int:message_id>")
def delete(message_id):
    message = Message.query.get(message_id)
    db.session.delete(message)
    db.session.commit()

    return redirect(url_for("index"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
