"""Init the app"""

import sqlite3
from flask import Flask, render_template, request, flash, redirect, abort, session
from website_manager import WebsiteManager
from reports_manager import ReportsManager
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
        data = {
            "form_validation_limit": app.config["FORM_VALIDATION_LIMIT"]
        }
        return render_template("index.html", **data)
    abort(405)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new account"""
    if request.method == "GET":
        session["csrf_token"] = service.create_csrf_token()
        data = {
            "filled": {},
            "form_validation_limit": app.config["FORM_VALIDATION_LIMIT"]
        }
        return render_template("register.html", **data)

    if request.method == "POST":
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
            data = {
                "filled": filled,
                "form_validation_limit": app.config["FORM_VALIDATION_LIMIT"]
            }
            return render_template("register.html", **data)
        if password1 != password2:
            flash("Passwords do not match")
            filled = {"username": username}
            data = {
                "filled": filled,
                "form_validation_limit": app.config["FORM_VALIDATION_LIMIT"]
            }
            return render_template("register.html", **data)
        if len(password1) < config.PASSWORD_MIN_LENGTH:
            flash(f"Password must be at least {config.PASSWORD_MIN_LENGTH} characters long")
            filled = {"username": username}
            data = {
                "filled": filled,
                "form_validation_limit": app.config["FORM_VALIDATION_LIMIT"]
            }
            return render_template("register.html", **data)

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
    service.require_login()
    page, limit, offset = service.get_pagination_parameters()
    manager = WebsiteManager(session["user_id"])
    data = manager.get_dashboard_websites({"page": page, "limit": limit, "offset": offset})
    return render_template("main.html", **data)

@app.route("/add-website", methods=["POST"])
def add_website():
    """Add new website to user database"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
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
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        website_visibility = request.form["website_visibility"]
        if service.validate_edit_permission(session["user_id"], website_id):
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
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        if service.validate_edit_permission(session["user_id"], website_id):
            try:
                service.delete_website(website_id)
                return redirect("/website")
            except sqlite3.IntegrityError as e:
                flash(str(e))
                return redirect("/website")
    abort(403)

@app.route("/copy-website", methods=["POST"])
def copy_website():
    """Copy Public Website to User Database"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["public_website_id"]
        if service.validate_copy_permission(website_id):
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
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        session.clear()
        return redirect("/")
    abort(405)

@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    """Render User Profile"""
    service.require_login()
    if request.method == "GET":
        profile_owner = user_id == session.get("user_id")
        page, limit, offset = service.get_pagination_parameters("page", 5)
        reports_page, reports_limit, reports_offset = (
            service.get_pagination_parameters("reports_page", 10)
        )
        manager = WebsiteManager(session["user_id"])
        data = manager.get_profile_data(
            user_id, profile_owner, {"page": page, "limit": limit, "offset": offset}
        )
        reports_manager = ReportsManager()
        reports_data = reports_manager.get_profile_reports(
            user_id,
            profile_owner,
            {
            "page": reports_page,
            "limit": reports_limit,
            "offset": reports_offset
            }
        )
        data.update(reports_data)
        return render_template("profile.html", **data)
    abort(405)

@app.route("/website", methods=["GET"])
def website():
    """Render Websites"""
    service.require_login()
    page, limit, offset = service.get_pagination_parameters("page", 5)
    public_page, public_offset = service.get_pagination_parameters(
        "public_page", 5, return_limit=False
    )
    filter_query = request.args.get("filter", "").strip()
    manager = WebsiteManager(session["user_id"])
    data = manager.get_websites(
        {"page": page, "limit": limit, "offset": offset},
        {"page": public_page, "offset": public_offset},
        filter_query
    )
    return render_template("website.html", **data)

@app.route("/website/<int:url_id>", methods=["GET"])
def website_info(url_id):
    """Render Website Info"""
    service.require_login()
    if request.method == "GET":
        if service.check_website_view_permission(url_id, session["user_id"]):
            manager = WebsiteManager(session["user_id"])
            website_data_dict = manager.get_website_details(url_id)
            reports_page, reports_limit, reports_offset = (
                service.get_pagination_parameters("reports_page", 10)
            )
            reports_manager = ReportsManager()
            reports_data = reports_manager.get_website_reports(
                url_id, {"page": reports_page, "limit": reports_limit, "offset": reports_offset}
            )
            data = {
                "website_data": website_data_dict["website_data"],
                "priority_classes": website_data_dict["priority_classes"],
            }
            data.update(reports_data)
            return render_template("website_info.html", **data)
    abort(403)

@app.route("/website/<int:url_id>/report", methods=["POST"])
def website_report(url_id):
    """Report website status"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        if service.validate_report_permission(session["user_id"], url_id):
            service.report_website_by_id(url_id, session["user_id"])
            manager = WebsiteManager(session["user_id"])
            website_data_dict = manager.get_website_details(url_id)
            reports_page, reports_limit, reports_offset = (
                service.get_pagination_parameters("reports_page", 10)
            )
            reports_manager = ReportsManager()
            reports_data = reports_manager.get_website_reports(
                url_id, {"page": reports_page, "limit": reports_limit, "offset": reports_offset}
            )
            data = {
                "website_data": website_data_dict["website_data"],
                "priority_classes": website_data_dict["priority_classes"],
            }
            data.update(reports_data)
            return render_template("website_info.html", **data)
    abort(403)

@app.route("/update-priority", methods=["POST"])
def update_priority():
    """Update website priority"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        priority = request.form["priority"]
        if not service.validate_priority_class(priority):
            abort(405)
        if service.validate_edit_permission(session["user_id"], website_id):
            service.update_website_priority(website_id, priority)
            return redirect(f"/website/{website_id}")
    abort(403)
