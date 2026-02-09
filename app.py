from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return "Username sudah digunakan"
        conn.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/profile")
        else:
            return "Login gagal"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def index():
    return redirect("/login")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html")


@app.route("/about")
def about():
    if "user" not in session:
        return redirect("/login")
    return render_template("about.html")


@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")
    return render_template("profile.html", username=session["user"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
