"""Init the app"""

import urllib
from flask import Flask, render_template, request
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route("/ping")
def ping():
    """For testing connection to the localhost"""
    return render_template("ping.html")
