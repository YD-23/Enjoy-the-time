import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash  # From pset 9 finance

from helpers import apology, login_required, lookup, usd   # From pset 9 finance

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pesona.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user
    session.clear()

    # Reach via POST (submit form)
    if request.method == "POST":
        
        # Initiate user input as variable
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(password)
        
        # Alert if empty username submitted
        if not username:
            # Flash notification
            flash("Username belum terisi")
            return render_template("register.html")
        
        # Alert if empty password submitted
        elif not password:
            # Flash notification
            flash("Password belum terisi")
            return render_template("register.html")
        
        # Alert if empty password submitted
        elif not confirmation:
            # Flash notification
            flash("Password konfirmasi belum terisi")
            return render_template("register.html")

        # Alert if password and confirmation password not match
        elif password != confirmation:
            # Flash notification
            flash("Password tidak sama, masukkan password yang sama")
            return render_template("register.html")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Alert if username already exist
        if len(rows) != 0:  # Kode ini menunjukkan banyak karakter pada data(row) tidak sama dengan satu, arti lainnya adalah ada hasil dari pencarian data username
            # Flash notification
            flash("Username sudah ada, gunakan username yang lain!")
            return render_template("register.html")
        
        # Insert new user data into database
        db.execute("INSERT INTO users (username, password) VALUES(? , ?)", username, password_hash)

        # Flash notification
        flash(f"Berhasil masuk sebagai {username}")
        
        # Redirect user to login page
        return redirect("/login")
    
    # Reach via GET (by URL)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Password belum terisi")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password belum terisi")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Username / password tidak valid")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]  # Rows [0]["id"] artinya, hasil pencarian (rows) pasti hanya akan menemukan satu data (satu baris data), ingat baris pertama adalah rows[0], sehingga rows[0]["id"] adalah baris pertama dan kolom "id" menghasilkan "id user" 

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
def index():

    if request.method == "GET":
        return render_template('index.html')


@app.route("/lokasi1", methods=["GET", "POST"])
def lokasi1():
    # Define the page number
    destination = 1

    # Reach by submit form (POST)
    if request.method == "POST":

        # Cek apakah pengguna sudah login, jika belum arahkan ke halaman login
        if "user_id" not in session:
            flash("Silahkan login dahulu sebelum mengirimkan komentar")
            return redirect("/login")
        
        # JIka sudah login, Get user id
        user_id = session["user_id"]

        # Inisialisasi variabel
        comment = request.form.get("comment")
        rating = request.form.get("rating")

        # Kondisi jika user tidak memasukkan komentar atau rating
        if not comment or not rating:
            flash("Belum memasukkan komentar/rating")
        else:
            # Insert data ke database
            db.execute("INSERT INTO reviews (review_id, comment, rating, destination) VALUES (?, ?, ?, ?)", user_id, comment, rating, destination)
        
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)

        return render_template("lokasi1.html", reviews=reviews)

    else:
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)
        # Reach by url (GET)
        return render_template("lokasi1.html", reviews=reviews)


@app.route("/lokasi2", methods=["GET", "POST"])
def lokasi2():

     # Define the page number
    destination = 2

    # Reach by submit form (POST)
    if request.method == "POST":

        # Cek apakah pengguna sudah login, jika belum arahkan ke halaman login
        if "user_id" not in session:
            flash("Silahkan login dahulu sebelum mengirimkan komentar")
            return redirect("/login")
        
        # JIka sudah login, Get user id
        user_id = session["user_id"]

        # Inisialisasi variabel
        comment = request.form.get("comment")
        rating = request.form.get("rating")

        # Kondisi jika user tidak memasukkan komentar atau rating
        if not comment or not rating:
            flash("Belum memasukkan komentar/rating")
        else:
            # Insert data ke database
            db.execute("INSERT INTO reviews (review_id, comment, rating, destination) VALUES (?, ?, ?, ?)", user_id, comment, rating, destination)
        
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)

        return render_template("lokasi2.html", reviews=reviews)

    else:
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)
        # Reach by url (GET)
        return render_template("lokasi2.html", reviews=reviews)


@app.route("/lokasi3", methods=["GET", "POST"])
def lokasi3():

    # Define the page number
    destination = 3

    # Reach by submit form (POST)
    if request.method == "POST":

        # Cek apakah pengguna sudah login, jika belum arahkan ke halaman login
        if "user_id" not in session:
            flash("Silahkan login dahulu sebelum mengirimkan komentar")
            return redirect("/login")
        
        # Get user id
        user_id = session["user_id"]

        # Inisialisasi variabel
        comment = request.form.get("comment")
        rating = request.form.get("rating")

        # Kondisi jika user tidak memasukkan komentar atau rating
        if not comment or not rating:
            flash("Belum memasukkan komentar/rating")
        else:
            # Insert data ke database
            db.execute("INSERT INTO reviews (review_id, comment, rating, destination) VALUES (?, ?, ?, ?)", user_id, comment, rating, destination)
        
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ?", destination)

        return render_template("lokasi3.html", reviews=reviews)

    else:
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time ASC", destination)
        # Reach by url (GET)
        return render_template("lokasi3.html", reviews=reviews)



@app.route("/lokasi4", methods=["GET", "POST"])
def lokasi4():

    # Define the page number
    destination = 4

    # Reach by submit form (POST)
    if request.method == "POST":

        # Cek apakah pengguna sudah login, jika belum arahkan ke halaman login
        if "user_id" not in session:
            flash("Silahkan login dahulu sebelum mengirimkan komentar")
            return redirect("/login")
        
        # Get user id
        user_id = session["user_id"]

        # Inisialisasi variabel
        comment = request.form.get("comment")
        rating = request.form.get("rating")

        # Kondisi jika user tidak memasukkan komentar atau rating
        if not comment or not rating:
            flash("Belum memasukkan komentar/rating")
        else:
            # Insert data ke database
            db.execute("INSERT INTO reviews (review_id, comment, rating, destination) VALUES (?, ?, ?, ?)", user_id, comment, rating, destination)
        
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)

        return render_template("lokasi4.html", reviews=reviews)

    else:
        # Ambil data review untuk ditampilkan
        reviews = db.execute("SELECT users.username, reviews.comment, reviews.rating FROM users JOIN reviews ON users.id = reviews.review_id WHERE reviews.destination = ? ORDER BY time DESC", destination)
        # Reach by url (GET)
        return render_template("lokasi4.html", reviews=reviews)