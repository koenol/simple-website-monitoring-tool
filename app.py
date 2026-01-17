"""Init the app"""

from flask import Flask, render_template
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

if app.secret_key is None:
    raise RuntimeError("Cannot find secret_key in config.")

@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")
