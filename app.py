from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from helpers import *
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["GET"])
@login_required
def index():
    """
    Renders the index.html template and passes the user's todos and email to it.
    """
    todos = get_todos(session["user_id"][0][0])
    return render_template("index.html", todos=todos, email=session["email"])

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login. If the request method is GET, renders the login.html template.
    If the request method is POST, attempts to sign in the user and redirects to the index page
    if successful, or renders the login.html template with an error message if unsuccessful.
    """
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        logged_in = signin(email, password)
        if logged_in:
            session["email"] = email
            session["user_id"] = get_userid(email)
            return redirect("/")
        else:
            return render_template("login.html", message="invalid email or password")

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handles user registration. If the request method is GET, renders the register.html template.
    If the request method is POST, attempts to sign up the user and renders the register.html template
    with a message indicating the result of the operation.
    """
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmpassword")
        hashed_password = generate_password_hash(password)
        if email == '' or password == '':
            return render_template("register.html", message='email or password is missing')
        if password != confirmation:
            return render_template("register.html", message='passwords do not match')
        created = signup(email, hashed_password)
        return render_template("register.html", message=created)

@app.route("/logout")
def logout():
    """
    Clears the user's session and redirects to the login page.
    """
    session.clear()
    return redirect("/login")

@app.route("/addtodo", methods=['POST'])
@login_required
def todo():
    """
    Adds a new todo item for the logged-in user.
    """
    data = request.get_json()
    task = data.get('task')
    id = session["user_id"][0][0]
    add_todo(id, task)
    return jsonify({'message': 'Task added successfully'}), 200

@app.route("/deletetodo", methods=['POST'])
@login_required
def delete():
    """
    Deletes a todo item for the logged-in user.
    """
    data = request.get_json()
    task = data.get('task')
    id = session["user_id"][0][0]
    deleted = delete_todo(id, task)
    if deleted:
        return jsonify({'message': 'Task removed successfully'}), 200
    else:
        return jsonify({'message': 'An error occurred'}), 500

@app.route("/updatetime", methods=["POST"])
@login_required
def time():
    """
    Updates the time for a todo item for the logged-in user.
    """
    data = request.get_json()
    time = int(data.get('time'))
    text = str(data.get('text'))
    id = session["user_id"][0][0]
    updated = update_time(time, id, text)
    if updated:
        return jsonify({'message': 'updated'}), 200
    else:
        return jsonify({'message': 'An error occurred'}), 400

@app.route("/gettime", methods=["POST"])
@login_required
def gettime():
    """
    Retrieves the time for a todo item for the logged-in user.
    """
    data = request.get_json()
    text = str(data.get('text'))
    id = session["user_id"][0][0]
    time = gettimefromdb(text, id)
    if time[0][0] >= 0:
        return jsonify({'message': time[0][0]}), 200
    else:
        return jsonify({'message': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)


#start the clock once the start timer button is clicked


# pallette https://colorhunt.co/palette/d2e0fbf9f3ccd7e5ca8eaccd

