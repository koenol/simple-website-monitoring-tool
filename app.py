"""Init the app"""

import sqlite3
from flask import Flask, render_template, request, flash, redirect, abort
import config
import service


app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["FORM_VALIDATION_LIMIT"] = [
    config.USERNAME_MIN_LENGTH,
    config.USERNAME_MAX_LENGTH,
    config.PASSWORD_MIN_LENGTH
]

@app.route("/", methods=["GET", "POST"])
def index():
    """Render the home page."""
    if request.method == "GET":
        return render_template(
            "index.html", 
            form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )
    abort(405)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new account"""
    if request.method == "GET":
        return render_template(
            "register.html", filled={}, 
            form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not service.valid_username(username):
            flash(
                f"Username must be between {config.USERNAME_MIN_LENGTH} "
                f"and {config.USERNAME_MAX_LENGTH} characters.\n"
                "It must contain only letters."
            )
            filled = {"username": username}
            return render_template("register.html",
                filled=filled, form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )
        if password1 != password2:
            flash("Passwords do not match")
            filled = {"username": username}
            return render_template("register.html",
                filled=filled, form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )
        if len(password1) < config.PASSWORD_MIN_LENGTH:
            flash(f"Password must be at least {config.PASSWORD_MIN_LENGTH} characters long")
            filled = {"username": username}
            return render_template("register.html",
                filled=filled, form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )

        try:
            service.create_user(username, password1)
        except sqlite3.IntegrityError as e:
            if (str(e)) == "UNIQUE constraint failed: users.username":
                flash("Username already exists.")
            else:
                flash("Something went wrong, please contact adminstrator.")
            return redirect("/register")

        flash("Registration Successful. You may now log in.")
        return redirect("/")
    abort(405)

@app.route("/login")
def login():
    """Login to website"""

@app.route("/ping")
def ping():
    """For testing connection to the localhost"""
    return render_template("ping.html")
