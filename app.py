"""Init the app"""

from flask import Flask, render_template, request, flash, redirect, abort
import config
import service

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["FORM_VALIDATION_LIMIT"] = [
    config.USERNAME_MIN_LENGTH,
    config.USERNAME_MAX_LENGTH,
    config.PASSWORD_MIN_LENGTH,
    config.PASSWORD_MAX_LENGTH
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
            flash("Username must be between 3 and 12 characters and it must contain only letters.")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
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
