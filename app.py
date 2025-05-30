
from flask import Flask, render_template, request, redirect, url_for, session
import fuel_manager
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/", methods=["GET"])
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    fuel_data = fuel_manager.read_fuel_data()
    return render_template("index.html", fuel_data=fuel_data, role=session.get("role"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        user = users.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        users = load_users()
        if username in users:
            return "Username already exists", 409

        users[username] = {"password": password, "role": role}
        save_users(users)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/update_fuel", methods=["POST"])
def update_fuel():
    if "username" not in session:
        return redirect(url_for("login"))

    # Staff is allowed to update fuel but only sales (negative amounts)
    if session["role"].lower() == "staff":
        fuel_type = request.form.get("fuel_type")
        amount = float(request.form.get("amount"))
        if amount > 0:
            return "Access Denied: Staff can only update sales (negative values).", 403
        fuel_manager.update_fuel(fuel_type, amount, is_sale=True)
    elif session["role"].lower() == "manager":
        fuel_type = request.form.get("fuel_type")
        amount = float(request.form.get("amount"))
        fuel_manager.update_fuel(fuel_type, amount, is_sale=(amount < 0))
    else:
        return "Access Denied", 403

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session
import fuel_manager
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route("/", methods=["GET"])
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    fuel_data = fuel_manager.read_fuel_data()
    return render_template("index.html", fuel_data=fuel_data, role=session.get("role"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = load_users()
        user = users.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        users = load_users()
        if username in users:
            return "Username already exists", 409

        users[username] = {"password": password, "role": role}
        save_users(users)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/update_fuel", methods=["POST"])
def update_fuel():
    if "username" not in session:
        return redirect(url_for("login"))

    # Staff is allowed to update fuel but only sales (negative amounts)
    if session["role"].lower() == "staff":
        fuel_type = request.form.get("fuel_type")
        amount = float(request.form.get("amount"))
        if amount > 0:
            return "Access Denied: Staff can only update sales (negative values).", 403
        fuel_manager.update_fuel(fuel_type, amount, is_sale=True)
    elif session["role"].lower() == "manager":
        fuel_type = request.form.get("fuel_type")
        amount = float(request.form.get("amount"))
        fuel_manager.update_fuel(fuel_type, amount, is_sale=(amount < 0))
    else:
        return "Access Denied", 403

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)

