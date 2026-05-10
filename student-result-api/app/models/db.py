from app import mysql


def query_one(sql, params=None):
    """Run a SELECT and return a single row as a dict."""
    cur = mysql.connection.cursor()
    cur.execute(sql, params or [])
    return cur.fetchone()


def query_all(sql, params=None):
    """Run a SELECT and return all rows as a list of dicts."""
    cur = mysql.connection.cursor()
    cur.execute(sql, params or [])
    return cur.fetchall()


def execute(sql, params=None):
    """Run an INSERT / UPDATE / DELETE and commit. Returns the cursor."""
    cur = mysql.connection.cursor()
    cur.execute(sql, params or [])
    mysql.connection.commit()
    return cur
