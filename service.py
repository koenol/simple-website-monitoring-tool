"""Service methods"""

import re
import secrets
from flask import session, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import urllib.request, urllib.error

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
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

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

def add_website(user_id, address, keyword):
    """Insert domain into the database"""
    ## domain = address
    ## kword = keyword // not in use for now
    sql = "INSERT INTO urls (user_id, addr, public) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, address, False])


def valid_address(address):
    """check if address format is valid"""
    pattern = re.compile(r"^[a-z0-9-]+\.[a-z]{2,}$")
    return pattern.fullmatch(address)

def get_user_websites(user_id):
    """Get all user websites"""
    sql = "SELECT addr, id, public FROM urls WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result

def get_public_websites():
    """Get all public websites"""
    sql = "SELECT addr, id FROM urls WHERE public = ?"
    result = db.query(sql, [True])
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

def get_public_websites_filtered(filter_query):
    """Get Filtered Public Websites"""
    sql = "SELECT addr, id FROM urls WHERE public = ? AND addr LIKE ?"
    website_filter = f"%{filter_query}%"
    result = db.query(sql, [True, website_filter])
    return result

def copy_website(user_id, website_id):
    """Copy Public Website to User Database"""
    sql = "SELECT addr FROM urls WHERE id = ?"
    result = db.query(sql, [website_id])
    sql = "INSERT INTO urls (user_id, addr, public) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, result[0]["addr"], False])

def ping_all_monitored_websites(user_id):
    results = get_user_websites(user_id)
    for url in results:
        print(ping_website(url["addr"]))

def ping_website(url_addr):
    try:
        req = urllib.request.Request(("https://" + url_addr), headers={"User-Agent": "Mozilla/5.0"})
        response = urllib.request.urlopen(req, timeout=3)
        return True, response.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except urllib.error.URLError as e:
        return False, None
    
def update_website_status(url_id):
    pass