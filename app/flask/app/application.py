import os, requests
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "bjGrTjIMHYECVtVv7XziA", "isbns": "9781632168146"})

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



# Routes

@app.route("/")
def home():
    # Setting user ID
    session["user_id"] = "To_be_set"
    user_id = session["user_id"]
    # End setting user ID
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Setting user ID
    session["user_id"] = "To_be_set"
    user_id = session["user_id"]
    # End setting user ID
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            return render_template("register.html", reg_error="This username already exists. Please choose another one.")
        if len(username) < 3: 
            return render_template("register.html", reg_error="Your username must be at least three characters long.")
        if len(password) < 5: 
            return render_template("register.html", reg_error="Your password must be at least five characters long.")
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
        db.commit()
        return render_template("registered.html")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Setting user ID
    user_id = session["user_id"]
    # End setting user ID
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 0:
                return render_template("login.html", login_error="The password you entered is not the right one for this username.")
            else:
                #Here the result is given as a tuple containing one term, so the following line retrives its first term to set the user ID.
                session["user_id"] = (db.execute("SELECT id FROM users WHERE username = :username", {"username": username}).fetchone())[0]
                user_id = session["user_id"]
                return render_template("search.html", temp = 1)
        else:
            return render_template("login.html", login_error="Wrong username.")
    else:
        return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    # Setting user ID
    user_id = session["user_id"]
    # End setting user ID
    try:
        user_id > 0
        if request.method == "POST":
            keywords = request.form.get("keywords")
            if len(keywords) == 0:
                return render_template("search.html", error = "You need to type something in the search bar in order to find books.")
            # Here a 'query' variable is created to avoid SQL injections later (e.g. when passing single quotes)
            query = "%" + request.form.get("keywords") + "%"
            results = db.execute("SELECT * FROM books WHERE isbn::TEXT ILIKE :query OR title ILIKE :query OR author ILIKE :query ORDER BY title",{"query": query}).fetchall()
            if db.execute("SELECT * FROM books WHERE isbn::TEXT ILIKE :query OR title ILIKE :query OR author ILIKE :query ORDER BY title",{"query": query}).rowcount == 0:
                return render_template("search.html", error = "Sorry, we found no book corresponding to those keywords.")
            return render_template("results.html", results = results, keywords = keywords)
        else:
            return render_template("search.html")
    except:
        return render_template("home.html", message="You need to sign in before being able to access book reviews.")

@app.route("/book/<string:isbn>", methods = ["GET","POST"])
def book(isbn):
    # Setting user ID
    user_id = session["user_id"]
    # End setting user ID
    try:
        user_id > 0
        book = db.execute(str(f"SELECT * FROM books WHERE isbn = '{isbn}'")).fetchone()
        # Adding zeros to the ISBN when <10 figures so it matches the ISBN of Goodreads
        isbns = isbn.zfill(10)
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "bjGrTjIMHYECVtVv7XziA", "isbns": isbns})
        ratingNum = ((res.json()["books"])[0])["work_ratings_count"]
        ratingAvg = ((res.json()["books"])[0])["average_rating"]
        if db.execute(str(f"SELECT * FROM reviews WHERE isbn = '{isbn}' AND user_id = '{user_id}'")).rowcount > 0:
            selfRated = "yes"
        else:
            selfRated = "no"
        if request.method == "POST":
            if selfRated == "yes":
                noReview = "no"
                reviews = db.execute(str(f"SELECT * FROM reviews INNER JOIN users ON users.id = user_id WHERE isbn = '{isbn}'")).fetchall()
                return render_template("book.html", book = book, reviews = reviews, ratingNum = ratingNum, ratingAvg = ratingAvg, selfRated = selfRated, noReview = "no", message="You already submitted a review for this book.")
            rating = int(request.form.get("rating"))
            comment = request.form.get("comment")
            db.execute("BEGIN")
            db.execute("INSERT INTO reviews (rating, comment, isbn, user_id) VALUES (:rating, :comment, :isbn, :user_id)",{"rating": rating, "comment": comment, "isbn": isbn, "user_id": user_id})
            db.execute("COMMIT")
            db.commit()
            selfRated = "yes"
        reviews = db.execute(str(f"SELECT * FROM reviews INNER JOIN users ON users.id = user_id WHERE isbn = '{isbn}'")).fetchall()
        if db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
            noReview = "yes"
        else:
            noReview = "no"
        return render_template("book.html", book = book, reviews = reviews, ratingNum = ratingNum, ratingAvg = ratingAvg, selfRated = selfRated, noReview = noReview)
    except:
        return render_template("home.html", message="You need to sign in before being able to access book reviews.")

@app.route("/api/<string:isbn>")
def book_api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422
    # Adding zeros to the ISBN when <10 figures so it matches the ISBN of Goodreads
    isbns = isbn.zfill(10)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "bjGrTjIMHYECVtVv7XziA", "isbns": isbns})
    ratingNum = ((res.json()["books"])[0])["work_ratings_count"]
    ratingAvg = float(((res.json()["books"])[0])["average_rating"])
    return jsonify({
    "title": book.title,
    "author": book.author,
    "year": book.year,
    "isbn": book.isbn,
    "review_count": ratingNum,
    "average_score": ratingAvg
})
