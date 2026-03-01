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
    service.require_login()
    page, limit, offset = service.get_pagination_parameters()
    service.ping_all_monitored_websites(session["user_id"], limit, offset)
    total_websites = service.count_user_websites(session["user_id"])
    personal_websites = service.get_user_websites(session["user_id"], limit, offset)
    total_pages = service.calculate_total_pages(total_websites, limit)
    return render_template("main.html",
                         personal_websites=personal_websites,
                         page=page,
                         total_pages=total_pages,
                         total_websites=total_websites)

@app.route("/add-website", methods=["GET", "POST"])
def add_website():
    """Add new website to user database"""
    service.require_login()
    if request.method == "GET":
        return render_template("add_website.html")

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
        userdata = service.get_user_data_public(user_id)
        page, limit, offset = service.get_pagination_parameters("page", 5)
        reports_page, reports_limit, reports_offset = (
            service.get_pagination_parameters("reports_page", 10)
        )
        reports_count = service.get_count_website_reports_created(user_id)
        if profile_owner:
            total_websites = service.count_user_websites(user_id)
            websites = service.get_user_websites(user_id, limit, offset)
            total_reports = service.get_user_websites_reports_count(user_id)
            reports = service.get_user_websites_reports_all(user_id, reports_limit, reports_offset)
        else:
            total_websites = service.count_user_websites_public_only(
                user_id
            )
            websites = service.get_user_websites_public_only(
                user_id, limit, offset
            )
            total_reports = (
                service.get_user_websites_reports_count_public_only(user_id)
            )
            reports = service.get_user_websites_reports_public_only(
                user_id,
                reports_limit,
                reports_offset
            )
        reports = service.format_reports_iso_to_readable_format(reports)
        total_pages = service.calculate_total_pages(total_websites, limit)
        reports_total_pages = service.calculate_total_pages(total_reports, reports_limit)
        return render_template(
            "profile.html",
            personal_websites=websites,
            reports=reports,
            userdata=userdata,
            reports_count=reports_count,
            page=page,
            total_pages=total_pages,
            total_websites=total_websites,
            reports_page=reports_page,
            reports_total_pages=reports_total_pages,
            profile_owner=profile_owner
        )
    abort(405)

@app.route("/website", methods=["GET"])
def website():
    """Render Websites"""
    service.require_login()
    if request.method == "GET":
        page, limit, offset = service.get_pagination_parameters("page", 5)
        public_page, public_offset = service.get_pagination_parameters(
            "public_page", 5, return_limit=False
        )
        service.ping_all_monitored_websites(session["user_id"], limit, offset)
        total_websites = service.count_user_websites(session["user_id"])
        personal_websites = service.get_user_websites(session["user_id"], limit, offset)
        total_pages = service.calculate_total_pages(total_websites, limit)
        filter_query = request.args.get("filter", "").strip()
        total_public_websites = service.count_public_websites(session["user_id"], filter_query)
        total_public_pages = service.calculate_total_pages(total_public_websites, limit)
        if filter_query:
            public_websites = (
                service.get_public_websites_filtered(
                    filter_query, session["user_id"], limit, public_offset
                )
            )
        else:
            public_websites = service.get_public_websites(session["user_id"], limit, public_offset)
        return render_template(
            "website.html",
            personal_websites=personal_websites,
            public_websites=public_websites,
            filter_query=filter_query,
            page=page,
            total_pages=total_pages,
            total_websites=total_websites,
            public_page=public_page,
            total_public_pages=total_public_pages,
            total_public_websites=total_public_websites
        )
    abort(405)

@app.route("/website/<int:url_id>", methods=["GET"])
def website_info(url_id):
    """Render Website Info"""
    service.require_login()
    if request.method == "GET":
        if service.check_website_view_permission(url_id, session["user_id"]):
            website_data = service.get_website_info_by_id(url_id)
            reports_page, reports_limit, reports_offset = (
                service.get_pagination_parameters("reports_page", 10)
            )
            total_reports = service.count_website_reports_by_id(url_id)
            reports = service.get_website_reports_by_id(url_id, reports_limit, reports_offset)
            formatted_reports = service.format_reports_iso_to_readable_format(reports)
            reports_total_pages = service.calculate_total_pages(total_reports, reports_limit)
            priority_classes = service.get_priority_classes()
            return render_template(
                "website_info.html",
                website_data=website_data[0],
                reports=formatted_reports,
                priority_classes=priority_classes,
                reports_page=reports_page,
                reports_total_pages=reports_total_pages
            )
    abort(403)

@app.route("/website/<int:url_id>/report", methods=["POST"])
def website_report(url_id):
    """Report website status"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        service.report_website_by_id(url_id, session["user_id"])
        reports_page, reports_limit, reports_offset = (
            service.get_pagination_parameters("reports_page", 10)
        )
        total_reports = service.count_website_reports_by_id(url_id)
        website_data = service.get_website_info_by_id(url_id)
        reports = service.get_website_reports_by_id(url_id, reports_limit, reports_offset)
        formatted_reports = service.format_reports_iso_to_readable_format(reports)
        reports_total_pages = service.calculate_total_pages(total_reports, reports_limit)
        priority_classes = service.get_priority_classes()
        return render_template(
            "website_info.html",
            website_data=website_data[0],
            reports=formatted_reports,
            priority_classes=priority_classes,
            reports_page=reports_page,
            reports_total_pages=reports_total_pages
            )
    abort(403)

@app.route("/update-priority", methods=["POST"])
def update_priority():
    """Update website priority"""
    service.require_login()
    if request.method == "POST":
        service.check_csrf()
        website_id = request.form["website_id"]
        priority = request.form["priority"]
        if service.validate_edit_permission(session["user_id"], website_id):
            service.update_website_priority(website_id, priority)
            return redirect(f"/website/{website_id}")
    abort(403)
