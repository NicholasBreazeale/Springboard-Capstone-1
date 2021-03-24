import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session

from forms import LoginForm, RegisterForm
from models import db, connect_db, User, Deck, Card, Review

app = Flask(__name__)

app.config["SECRET_KEY"] = "y7C8*#Suh$HNuUqj^H42%ZU6eKA*$RZiXvX02OlDYE&JHRVmZ#yhgc&RH9aY0D0q"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost/capstone1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)
db.create_all()

@app.route("/", methods=["GET"])
def home():
    """Home page."""

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""

    form = RegisterForm()
    if form.validate_on_submit():
        if not User.query.filter_by(username=form.username.data).first():
            user = User(username=form.username.data, image_url=form.image_url.data, date=datetime.datetime.utcnow())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            return redirect(f"/user/{user.id}")
        form.username.errors.append("Username taken.")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session["user_id"] = user.id
            return redirect(f"/user/{user.id}")
        flash("Invalid username or password.", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["POST"])
def logout():
    """Logout current user."""

    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

@app.route("/user/<int:user_id>", methods=["GET"])
def profile(user_id):
    """Display user profile."""

    return render_template("user.html", user=User.query.get_or_404(user_id))

#@app.route("/deck/<int:deck_id>", methods=["GET"])

#@app.route("/editor", methods=["GET", "POST"])