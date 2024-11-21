from datetime import datetime

from flask import Blueprint, render_template, request, session, redirect, abort
from flask_login import login_user, login_required, logout_user, current_user

from app import login_manager, db
from app.models import User, Event, Registration
from app.forms import login_form, register_form, create_event_form, register_event_form, statuses

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
    events = Event.query.all()
    registrations = {
        event.id: next(
            (reg.status for reg in event.registrations if reg.user_id == current_user.id),
            "unregistered"
        )
        for event in events
    }

    return render_template("pages/events.html", events=events, registrations=registrations)

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

@main.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    if current_user.role == "volunteer":
        return redirect("/events")

    if request.method == "POST":
        try:
            new_event = Event(
                title=request.form["title"],
                description=request.form["description"],
                date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
                location=request.form["location"],
                creator=current_user
            )
            db.session.add(new_event)
            db.session.commit()

        except Exception as e:
            print(e)
            return "Помилка", 500

        return redirect("/events")

    return render_template("pages/events_create.html", fields=create_event_form)

@main.route("/events/<int:event_id>/delete", methods=["DELETE"])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event:
        return "Не знайдено", 404

    if current_user.id != event.creator_id:
        return "Ні", 403

    Registration.query.filter_by(event_id=event_id).delete()

    db.session.delete(event)
    db.session.commit()

    events = Event.query.all()

    return render_template("_event_grid.html", events=events)


@main.route("/events/toggle-personal", methods=["GET"])
@login_required
def toggle_event_visibility():
    is_checked = request.args.get("checked", default=False, type=lambda val: val.lower() == 'true')

    if not is_checked:
        events = Event.query.all()
    else: 
        events = Event.query.join(Registration).filter(Registration.user_id == current_user.id).all()

    registrations = {
        event.id: next(
            (reg.status for reg in event.registrations if reg.user_id == current_user.id),
            "unregistered"
        )
        for event in events
    }

    return render_template("_event_grid.html", events=events, registrations=registrations)

@main.route("/events/<int:event_id>/register", methods=["GET", "POST"])
@login_required
def register_to_event(event_id):
    event = Event.query.get(event_id)

    if request.method == "POST":
        try:
            new_registration = Registration(
                name=request.form["name"],
                surname=request.form["surname"],
                phone=request.form["phone"],
                location=request.form["location"],
                user_id=current_user.id,
                event_id=event.id,
                status="pending"
            )
            db.session.add(new_registration)
            db.session.commit()
        except Exception as e:
            print(e)
            return "Error", 500

        return redirect("/events")


    return render_template("pages/events_register.html", event=event, fields=register_event_form)

@main.route("/events/<int:event_id>/manage", methods=["GET"])
@login_required
def manage_event(event_id):
    event = Event.query.get(event_id)
    registrations = Registration.query.filter_by(event_id=event_id).all()

    if not event:
        return "Не знайдено", 404

    if current_user.id != event.creator_id:
        return "Ні", 403

    return render_template("pages/events_manage.html", event=event, registrations=registrations, statuses=statuses)

@main.route("/registrations/<int:reg_id>/toggle", methods=["PUT"])
@login_required
def toggle_registration(reg_id):
    registration = Registration.query.get(reg_id)

    if registration.status == "pending":
        new_status = "confirmed"
    elif registration.status == "confirmed":
        new_status = "cancelled"
    else:
        new_status = "pending"

    registration.status = new_status
    db.session.commit()

    print(registration.status)

    return render_template("_registration.html", reg=registration, statuses=statuses)
