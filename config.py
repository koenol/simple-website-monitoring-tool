"""
GLOBAL VARIABLES
------------------
SECRET_KEY is used for session management and CSRF protection.
------------------
"""

import os

def load_env():
    """Load environment variables from a .env file"""
    if os.path.exists('.env'):
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped or '=' not in stripped:
                        continue
                    key, value = stripped.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    os.environ[key] = value
        except OSError as e:
            print(f"Error loading .env file: {e}")

load_env()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Cannot find secret_key in .env file.")