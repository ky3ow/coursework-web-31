from flask import Blueprint, render_template, request, session, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import login_manager, db
from app.models import User

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

@main.route("/profile", methods=["GET"])
def profile():
    return render_template("pages/profile.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect("/events")

        flash("Неправильні дані", "error")
        return redirect("/login")

    return render_template("pages/login.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(email=email, password=password)  # Hash password before saving in production
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("pages/register.html")

