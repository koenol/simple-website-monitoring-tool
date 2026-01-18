"""Init the app"""

import urllib
from flask import Flask, render_template, request
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def index():
    """Render the home page."""
    ## for testing purposes:
    status = []
    urls = [
        f"{request.host_url}ping",
        f"{request.host_url}ping-fail"
    ]
    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                status.append(response.getcode())
        except urllib.error.HTTPError as e:
            status.append(e.code)

    return render_template("index.html", status=status)

@app.route("/ping")
def ping():
    """For testing connection to the localhost"""
    return render_template("ping.html")
