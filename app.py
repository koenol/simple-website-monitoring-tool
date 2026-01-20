"""Init the app"""

from flask import Flask, render_template, request, flash
import config
import service

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route("/register")
def register():
    """Register new account"""
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not service.valid_username(username):
        flash("Username must be between 3 and 12 characters and it must contain only letters")
        filled = {"username": username}
        return render_template("register.html", filled=filled)
    
    return render_template("register.html")

@app.route("/ping")
def ping():
    """For testing connection to the localhost"""
    return render_template("ping.html")
