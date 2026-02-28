"""Service methods"""

import re
import secrets
import urllib.error
import urllib.request
from datetime import datetime
from flask import session, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db


def valid_username(username):
    """Validate username is a string that contains only characters and is within set parameters."""
    if not username or not username.isalpha():
        return False
    username = sanitize(username)
    return config.USERNAME_MIN_LENGTH <= len(username) <= config.USERNAME_MAX_LENGTH

def sanitize(text):
    """Sanitize text."""
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'on\w+=".*?"', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(javascript:|data:|vbscript:)', '', text, flags=re.IGNORECASE)
    return text

def create_user(username, password):
    """Generate password hash and create user"""
    timestamp = datetime.now().isoformat()
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, creation_date, password_hash) VALUES (?, ?, ?)"
    db.execute(sql, [username, timestamp, password_hash])

def validate_user(username, password):
    """Validate User Password"""
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return False
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        session["user_id"] = result[0]["id"]
        session["username"] = username
        return True
    return False

def create_csrf_token():
    """Check CSRF token if needed"""
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(16)
    return token

def check_csrf():
    """Compare session CSRF token & request form token"""
    form_token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")
    if not form_token or form_token != session_token:
        abort(403)

def add_website(user_id, address):
    """Insert domain into the database"""
    sql = "INSERT INTO urls (user_id, addr, public, priority_class) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, address, False, 2])


def valid_address(address):
    """check if address format is valid"""
    pattern = re.compile(r"^[a-z0-9-]+\.[a-z]{2,}$")
    return pattern.fullmatch(address)

def get_user_websites(user_id, limit=None, offset=None):
    """Get all user websites"""
    if limit:
        sql = (
            "SELECT addr, id, public, url_status_ok, url_code FROM urls "
            "WHERE user_id = ? "
            "ORDER BY priority_class DESC "
            "LIMIT ? OFFSET ?"
        )
        result = db.query(sql, [user_id, limit, offset])
    else:
        sql = (
            "SELECT addr, id, public, url_status_ok, url_code FROM urls "
            "WHERE user_id = ? "
            "ORDER BY priority_class DESC"
        )
        result = db.query(sql, [user_id])
    return result

def get_public_websites(user_id, limit=None, offset=None):
    """Get all public websites"""
    if limit:
        sql = (
            "SELECT id, addr, url_status_ok, url_code, priority_class FROM urls "
            "WHERE public = ? AND user_id != ? "
            "ORDER BY priority_class DESC "
            "LIMIT ? OFFSET ?"
        )
        result = db.query(sql, [True, user_id, limit, offset])
    else:
        sql = (
            "SELECT id, addr, url_status_ok, url_code, priority_class FROM urls "
            "WHERE public = ? AND user_id != ? "
            "ORDER BY priority_class DESC"
        )
        result = db.query(sql, [True, user_id])
    return result

def toggle_visiblity(website_id, visibility):
    """Toggle Website Visibility"""
    new_visibility_status = 1 - int(visibility)
    sql = "UPDATE urls SET public = ? WHERE id = ?"
    db.execute(sql, [new_visibility_status, website_id])

def delete_website(website_id):
    """Delete User Website"""
    sql = "DELETE FROM urls WHERE id = ?"
    db.execute(sql, [website_id])

def get_public_websites_filtered(filter_query, user_id, limit=None, offset=None):
    """Get Filtered Public Websites"""
    website_filter = f"%{filter_query}%"
    if limit:
        sql = (
            "SELECT id, addr, url_status_ok, url_code, priority_class FROM urls "
            "WHERE public = ? AND addr LIKE ? AND user_id != ? "
            "ORDER BY priority_class DESC "
            "LIMIT ? OFFSET ?"
        )
        result = db.query(sql, [True, website_filter, user_id, limit, offset])
    else:
        sql = (
            "SELECT id, addr, url_status_ok, url_code, priority_class FROM urls "
            "WHERE public = ? AND addr LIKE ? AND user_id != ? "
            "ORDER BY priority_class DESC"
        )
        result = db.query(sql, [True, website_filter, user_id])
    return result

def copy_website(user_id, website_id):
    """Copy Public Website to User Database"""
    sql = "SELECT addr FROM urls WHERE id = ?"
    result = db.query(sql, [website_id])
    sql = "INSERT INTO urls (user_id, addr, public) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, result[0]["addr"], False])

def ping_all_monitored_websites(user_id, limit=None, offset=None):
    """Ping all monitored websites"""
    results = get_user_websites(user_id, limit, offset)
    errors = []
    url_errors = []
    for url in results:
        status_ok, code = ping_website(url["addr"])

        if code:
            try:
                update_website_status(url["id"], status_ok, code)
            except ValueError as e:
                errors.append(e)
        else:
            url_errors.append(url["addr"])

def ping_website(url_addr):
    """Ping a website"""
    try:
        req = urllib.request.Request(
            ("https://" + url_addr),
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            return True, response.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except urllib.error.URLError:
        return False, None

def update_website_status(url_id, status_ok, code):
    """Update website status and HTTP code."""
    sql = "UPDATE urls SET url_status_ok = ?, url_code = ? WHERE id = ?"
    db.execute(sql, [status_ok, int(code), url_id])

def get_website_info_by_id(url_id):
    """Get website info by id"""
    sql = """
    SELECT u.username, w.id, w.user_id, w.addr, w.url_status_ok, w.url_code, w.public, w.priority_class 
    FROM urls w
    JOIN users u ON w.user_id = u.id
    WHERE w.id = ?
    """
    result = db.query(sql, [url_id])
    return result

def check_website_view_permission(url_id, user_id):
    """Verify View Permission"""
    sql = """
        SELECT id FROM urls
        WHERE (id = ? AND user_id = ?)
        OR (id = ? AND public = ?)
    """
    result = db.query(sql, [url_id, user_id, url_id, True])
    return bool(result)

def report_website_by_id(url_id, user_id):
    """Insert Website Current Status Into Reports Page"""
    timestamp = datetime.now().isoformat()
    sql = """
    INSERT INTO reports (url_id, user_id, report_date, url_status_ok, url_code)
    SELECT id, ?, ?, url_status_ok, url_code FROM urls WHERE id = ?
    """
    db.execute(sql, [user_id, timestamp, url_id])

def get_website_reports_by_id(url_id, limit=10, offset=0):
    """Get website reports by url_id"""
    sql = """
    SELECT u.username, r.user_id, r.report_date, r.url_status_ok, r.url_code FROM reports r
    JOIN users u ON r.user_id = u.id
    WHERE r.url_id = ?
    ORDER BY r.report_date DESC
    LIMIT ? OFFSET ?
    """
    result = db.query(sql, [url_id, limit, offset])
    return [dict(row) for row in result] if result else []

def format_reports_iso_to_readable_format(reports):
    """Convert reports ISO format date to readable format"""
    for report in reports:
        dt = datetime.fromisoformat(report["report_date"])
        report["report_date"] = dt.strftime("%Y-%m-%d %H:%M")
    return reports

def get_user_websites_reports_all(user_id, limit=10, offset=0):
    """Get all reports for websites owned by the user"""
    sql = (
        "SELECT r.id, r.url_id, r.report_date, r.url_status_ok, r.url_code, u.addr "
        "FROM reports r "
        "JOIN urls u ON r.url_id = u.id "
        "WHERE u.user_id = ? "
        "ORDER BY r.report_date DESC "
        "LIMIT ? OFFSET ?"
    )
    result = db.query(sql, [user_id, limit, offset])
    return [dict(row) for row in result] if result else []

def get_user_data_public(user_id):
    """Get public user data"""
    sql = "SELECT username, creation_date FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if result:
        user_data = dict(result[0])
        user_data["creation_date"] = format_date_iso_to_readable_format(user_data["creation_date"])
        return [user_data]
    return result

def get_priority_classes():
    """Get all priority classes"""
    sql = "SELECT id, class from priority_classes"
    result = db.query(sql)
    return [dict(row) for row in result] if result else []

def update_website_priority(url_id, priority):
    """Update website priority class"""
    sql = "UPDATE urls SET priority_class = ? WHERE id = ?"
    db.execute(sql, [priority, url_id])

def get_count_website_reports_created(user_id):
    """Get count of the website reports created by the user"""
    sql = "SELECT COUNT(id) AS count FROM reports WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0]["count"] if result else 0

def count_user_websites(user_id):
    """Count total number of user websites"""
    sql = "SELECT COUNT(id) AS count FROM urls WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result[0]["count"] if result else 0

def count_public_websites(user_id, filter_query=None):
    """Count public websites"""
    if filter_query:
        f_query = sanitize(filter_query)
        sql = (
            "SELECT COUNT(id) AS count FROM urls "
            "WHERE public = ? AND addr LIKE ? AND user_id != ?"
        )
        result = db.query(sql, [True, f_query, user_id])
    else:
        sql = "SELECT COUNT(id) AS count FROM urls WHERE public = ? AND user_id != ?"
        result = db.query(sql, [True, user_id])
    return result[0]["count"] if result else 0

def format_date_iso_to_readable_format(isoformat):
    """Convert ISO format date to readable format"""
    dt = datetime.fromisoformat(isoformat)
    return dt.strftime("%Y-%m-%d %H:%M")

def get_user_websites_reports_count(user_id):
    """Count all reports for websites owned by the user"""
    sql = (
        "SELECT COUNT(r.id) AS count "
        "FROM reports r "
        "JOIN urls u ON r.url_id = u.id "
        "WHERE u.user_id = ?"
    )
    result = db.query(sql, [user_id])
    return result[0]["count"] if result else 0

def count_website_reports_by_id(url_id):
    """Count total reports for a specific website"""
    sql = "SELECT COUNT(id) AS count FROM reports WHERE url_id = ?"
    result = db.query(sql, [url_id])
    return result[0]["count"] if result else 0