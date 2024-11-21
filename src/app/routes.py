from flask import Blueprint, render_template, request, session, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user

from app import login_manager, db
from app.models import User
from app.forms import login_form, register_form

main = Blueprint("main", __name__)

login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/", methods=["GET"])
def home():
    return render_template("pages/index.html")

@main.route("/events", methods=["GET"])
@login_required
def events():
    return render_template("pages/events.html")

@main.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.query.filter_by(email=email).first()

            if user and user.password == password:
                login_user(user)
                return redirect("/events")

            return "Неправильні дані", 401

        except Exception as e:
            print(e)
            return "Помилка", 500

    return render_template("pages/login.html", fields=login_form)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        user_role = request.form["user_role"]

        if password != password_confirm:
            return "Паролі мають співпадати", 401

        try:
            new_user = User(email=email, password=password, role=user_role)  # Hash password before saving in production
            db.session.add(new_user)
            db.session.commit()

        except Exception as e:
            print(e)
            return "Помилка", 500

        return redirect("/login")

    return render_template("pages/register.html", fields=register_form)

