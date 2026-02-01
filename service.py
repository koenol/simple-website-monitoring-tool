"""Service methods"""

import re
from flask import session, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import secrets

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
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(16)
    return token

def check_csrf():
    form_token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")
    if not form_token or form_token != session_token:
        abort(403)

def add_website(user_id, address, keyword):
    """Insert domain into the database"""
    domain = address
    ## kword = keyword // not in use for now
    sql = "INSERT INTO urls (user_id, addr, public) VALUES (?, ?, ?)"
    db.execute(sql, [user_id, address, False])


def valid_address(address):
    """check if address format is valid"""
    pattern = re.compile(r"^[a-z0-9-]+\.[a-z]{2,}$")
    return pattern.fullmatch(address)

def get_user_websites(user_id):
    sql = "SELECT addr, id FROM urls WHERE user_id = ?"
    result = db.query(sql, [user_id])
    return result

def get_public_websites():
    sql = "SELECT addr FROM urls WHERE public = ?"
    result = db.query(sql, [True])
    return result

def toggle_visiblity(website_id):
    sql = "UPDATE urls SET public = ? WHERE id = ?"
    db.execute(sql, [True, website_id])