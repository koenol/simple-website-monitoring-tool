"""Init the app"""

from flask import Flask, render_template
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")
