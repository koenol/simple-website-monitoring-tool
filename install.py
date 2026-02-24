"""Install script to create the SQLite database and a .env file with SECRET_KEY."""

import sqlite3
import os
import secrets

if not os.path.exists("database.db"):
    try:
        with sqlite3.connect("database.db") as db:
            database_cursor = db.cursor()
            try:
                with open("schema.sql", "r", encoding="utf-8") as schema:
                    database_cursor.executescript(schema.read())
            except OSError as e:
                print(f"Error reading schema.sql: {e}")
            try:
                with open("init.sql", "r", encoding="utf-8") as init_file:
                    database_cursor.executescript(init_file.read())
            except OSError as e:
                print(f"Error reading init.sql: {e}")

            db.commit()
    except sqlite3.Error as e:
        print(f"Error creating database.db: {e}")

    try:
        with open(".env", "w", encoding="utf-8") as config_file:
            secret_key = secrets.token_hex(32)
            config_file.write(f"SECRET_KEY = \"{secret_key}\"\n")
    except OSError as e:
        print(f"Error creating .env: {e}")
