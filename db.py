"""Database commands."""
import sqlite3
from flask import g

def get_connection():
    """Connect to a database"""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=None):
    """Execute a SQL statement"""
    if params is None:
        params = []
    with get_connection() as con:
        result = con.execute(sql, params)
        con.commit()
        g.last_insert_id = result.lastrowid

def last_insert_id():
    """Get the last row id."""
    return g.last_insert_id

def query(sql, params=None):
    """Execute a SQL query"""
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
