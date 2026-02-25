"""Init the app"""

import sqlite3
from flask import Flask, render_template, request, flash, redirect, abort, session
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
        session["csrf_token"] = service.create_csrf_token()
        return render_template(
            "index.html", 
            form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )
    abort(405)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new account"""
    if request.method == "GET":
        session["csrf_token"] = service.create_csrf_token()
        return render_template(
            "register.html", filled={}, 
            form_validation_limit=app.config["FORM_VALIDATION_LIMIT"]
            )

    if request.method == "POST":
        print()
        service.check_csrf()
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

@app.route("/login", methods=["POST"])
def login():
    """Login to website"""
    if request.method == "POST":
        service.check_csrf()
        username = request.form["username"]
        password = request.form["password"]

        if service.valid_username(username):
            if service.validate_user(username, password):
                return redirect("/main")
        flash("Invalid username or password")
        return redirect("/")
    abort(405)

@app.route("/main", methods=["GET", "POST"])
def main():
    """Render Main View"""
    service.ping_all_monitored_websites(session["user_id"])
    personal_websites = service.get_user_websites(session["user_id"])
    return render_template("main.html", personal_websites=personal_websites)

@app.route("/add-website", methods=["GET", "POST"])
def add_website():
    """Add new website to user database"""
    if request.method == "GET":
        return render_template("add_website.html")

    if request.method == "POST":
        address = request.form["address"]
        if service.valid_address(address):
            try:
                service.add_website(session["user_id"], address)
                return redirect("/website")
            except sqlite3.IntegrityError as e:
                flash(str(e))
                return redirect("/website")
        else:
            flash("Incorrect domain format, use: 'example.com'")
            return redirect("/website")
    abort(405)

@app.route("/toggle-visibility", methods=["POST"])
def toggle_visibility():
    """Toggle User Website Visibility"""
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        website_visibility = request.form["website_visibility"]
        try:
            service.toggle_visiblity(website_id, website_visibility)
            return redirect(f"/website/{website_id}")
        except sqlite3.IntegrityError as e:
            flash(str(e))
            return redirect(f"/website/{website_id}")
    abort(405)

@app.route("/delete-website", methods=["POST"])
def delete_website():
    """Delete User Website"""
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        try:
            service.delete_website(website_id)
            return redirect("/website")
        except sqlite3.IntegrityError as e:
            flash(str(e))
            return redirect("/website")
    abort(405)

@app.route("/copy-website", methods=["POST"])
def copy_website():
    """Copy Public Website to User Database"""
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["public_website_id"]
        try:
            service.copy_website(session["user_id"], website_id)
            return redirect("/website")
        except sqlite3.IntegrityError as e:
            flash(str(e))
            return redirect("/website")
    abort(405)

@app.route("/logout", methods=["POST"])
def logout():
    """Logout and clear session"""
    if request.method == "POST":
        service.check_csrf()
        session.clear()
        return redirect("/")
    abort(405)

@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    """Render User Profile"""
    if request.method == "GET":
        userdata = service.get_user_data_public(user_id)
        if user_id == session["user_id"]:
            reports_count = service.get_count_website_reports_created(user_id)
            websites = service.get_user_websites(user_id)
            reports = service.get_user_websites_reports_all(user_id)
            return render_template(
                "profile.html",
                personal_websites=websites,
                reports=reports,
                userdata=userdata,
                reports_count=reports_count
            )
    abort(405)

@app.route("/website", methods=["GET"])
def website():
    """Render Websites"""
    if request.method == "GET":
        service.ping_all_monitored_websites(session["user_id"])
        personal_websites = service.get_user_websites(session["user_id"])
        filter_query = request.args.get("filter", "").strip()
        if filter_query:
            public_websites = service.get_public_websites_filtered(filter_query, session["user_id"])
        else:
            public_websites = service.get_public_websites(session["user_id"])
        return render_template(
            "website.html",
            personal_websites=personal_websites,
            public_websites=public_websites,
            filter_query=filter_query
        )
    abort(405)

@app.route("/website/<int:url_id>", methods=["GET"])
def website_info(url_id):
    """Render Website Info"""
    if request.method == "GET":
        if service.check_website_view_permission(url_id, session["user_id"]):
            website_data = service.get_website_info_by_id(url_id)
            reports = service.get_website_reports_by_id(url_id)
            formatted_reports = service.format_iso_to_readable_format(reports)
            priority_classes = service.get_priority_classes()
            return render_template(
                "website_info.html",
                website_data=website_data[0],
                reports=formatted_reports,
                priority_classes=priority_classes
            )
    abort(403)

@app.route("/website/<int:url_id>/report", methods=["POST"])
def website_report(url_id):
    """Report website status"""
    if request.method == "POST":
        service.check_csrf()
        service.report_website_by_id(url_id, session["user_id"])
        website_data = service.get_website_info_by_id(url_id)
        reports = service.get_website_reports_by_id(url_id)
        formatted_reports = service.format_iso_to_readable_format(reports)
        return render_template(
            "website_info.html",
            website_data=website_data[0],
            reports=formatted_reports
            )
    abort(403)

@app.route("/update-priority", methods=["POST"])
def update_priority():
    """Update website priority"""
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        priority = request.form["priority"]
        if service.check_website_view_permission(
            website_id, session["user_id"]
        ):
            service.update_website_priority(website_id, priority)
            return redirect(f"/website/{website_id}")
    abort(403)
