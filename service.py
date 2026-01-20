"""Service methods"""

import re
import config

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
