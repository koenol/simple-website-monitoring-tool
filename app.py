"""Init app."""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    """Render index.html"""
    return render_template("index.html")
