import sqlite3
from werkzeug.security import check_password_hash
from flask import session, redirect
from functools import wraps

def signup(email, password):
    """
    Registers a new user in the database.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    try:
        # Insert the new user's email and hashed password into the users table
        db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        connection.commit()
        return "account successfully created, proceed to login"
    except:
        # If the email already exists, return an error message
        return "email already exists"
    finally:
        connection.close()

def signin(email, password):
    """
    Authenticates a user by checking the provided email and password against the database.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Retrieve the stored password hash for the given email
    db.execute("SELECT password FROM users WHERE email=?", (email,))
    stored_pass = db.fetchone()
    # Check if the provided password matches the stored password hash
    exists = check_password_hash(stored_pass[0], password)
    connection.close()
    return exists

def get_todos(id: int):
    """
    Retrieves all the todos for a given user.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Fetch all the todo texts for the given user ID
    db.execute("SELECT text FROM todos WHERE user_id = ?", (id,))
    todos = db.fetchall()
    connection.close()
    return todos

def add_todo(id, text):
    """
    Adds a new todo item for a given user.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Insert the new todo item with the given user ID and text
    db.execute("INSERT INTO todos(user_id, text) VALUES(?, ?)", (id, text))
    connection.commit()
    connection.close()

def delete_todo(id, text):
    """
    Deletes a todo item for a given user.
    """
    try:
        connection = sqlite3.connect("static/database.db")
        db = connection.cursor()
        # Delete the todo item with the given user ID and text
        db.execute("DELETE FROM todos WHERE user_id = ? AND text = ?", (id, text))
        connection.commit()
        return True
    except sqlite3.error as e:
        print(e)
        return False
    finally:
        connection.close()

def get_userid(email):
    """
    Retrieves the user ID for a given email address.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Fetch the user ID for the given email
    db.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    id = db.fetchall()
    connection.close()
    return id

def update_time(time, id, text):
    """
    Updates the time for a todo item for a given user.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Fetch the current time value for the todo item
    db.execute("SELECT time FROM todos WHERE user_id =?", (id,))
    stime = int(db.fetchall()[0][0])
    # Update the time value for the todo item with the given user ID and text
    db.execute("UPDATE todos SET time = ? WHERE user_id = ? AND text = ?", (stime + time, id, text))
    connection.commit()
    connection.close()
    return True

def gettimefromdb(text, id):
    """
    Retrieves the time for a todo item for a given user.
    """
    connection = sqlite3.connect("static\\database.db")
    db = connection.cursor()
    # Fetch the time value for the todo item with the given user ID and text
    db.execute("SELECT time FROM todos WHERE user_id = ? AND text = ?", (id, text))
    time = db.fetchall()
    connection.close()
    return time

def login_required(f):
    """
    Decorator to require login for a route.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in (user ID is present in the session)
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
