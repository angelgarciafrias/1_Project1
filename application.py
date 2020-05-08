import os

import requests
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

app.config["SESSION_PERMANET"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ukiqyxpjytmnqk:752de8d60c9db6736c5d9d6a7972a70228fad45de4dc1b466833f93108bcd018@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d23cjhe2n1foda"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Page for sign-up
@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        """ensure data was submitted"""
        if not (request.form.get("username") and request.form.get("password") and request.form.get("email")):
            return render_template("error2.html", message="You must provide all the information")

        """check if username is valid"""
        username_check = Users.query.get(request.form.get("username"))
        if username_check:
            return render_template("error2.html", message="Username already taken.")

        """add username and password to database"""
        u = Users(username=request.form.get("username"),email=request.form.get("email"))
        u.set_password(request.form.get("password"))
        db.session.add(u)
        db.session.commit()
        return render_template("index.html")

# Index page for sign-in
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        session.clear()
        return render_template("index.html")

    if request.method == "POST":
        """ clear the session of the user """
        session.clear()
        """ensure data was submitted"""
        if not (request.form.get("username") or request.form.get("password")):
            return render_template("error.html", message="You must fill all the information")

        """get username and password"""
        username = request.form.get("username")
        
        """check if username and password are valid"""
        u = Users.query.filter_by(username=username).first()
        session["username_session"] = username

        if (u and u.check_password(request.form.get("password_input"))):
            list_books = Books.query.all()
            return render_template("home.html",list_books=list_books,username_session=username)
        else:    
            return render_template("error.html", message="Wrong username or password.")

# search bar and book list
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        list_books = Books.query.all()
        return render_template("home.html",list_books=list_books)
    if request.method == "GET":
        return render_template("error.html", message="Please log in to access the website.")

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    
    details_books = Books.query.get(isbn)
    if not details_books:
        return render_template("error.html", message="Not a valid ISBN.")

    """list reviews from Goodread"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vzGNXaZ6kYSFlxZNkFVg", "isbns": isbn})
    reviews_count = res.json()["books"][0]["work_reviews_count"]
    average_rating = res.json()["books"][0]["average_rating"]

    try:
        current_user = session["username_session"]
    except:
        return render_template("error.html", message="Please log in to access the website.")

    """submit review"""
    if request.method == "POST":
        check_reviews = Reviews.query.filter_by(reviews_isbn=isbn,reviews_username=current_user).first()
        if check_reviews:
            return render_template("error2.html", message="You have already submitted a review for this book.")
        else:
            comment = request.form.get("comment")
            rating = request.form.get("rating")
            r = Reviews(text=comment,rating=rating,reviews_isbn=isbn,reviews_username=current_user)
            db.session.add(r)
            db.session.commit()
            """get reviews from users"""
    
    list_reviews = Reviews.query.filter_by(reviews_isbn=isbn).all()
    if list_reviews is None:
        list_reviews = []

    return render_template("book.html",details_books=details_books,list_reviews=list_reviews,current_user=current_user,reviews_count=reviews_count,average_rating=average_rating)

@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    
    """ get book details from database"""
    details_books = Books.query.get(isbn)
    if not details_books:
        return jsonify({"error": "Invalid ISBN"}), 404
    
    """ get book details from Goodread"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vzGNXaZ6kYSFlxZNkFVg", "isbns": isbn})
    reviews_count = res.json()["books"][0]["work_reviews_count"]
    average_rating = res.json()["books"][0]["average_rating"]

    return jsonify({
        "title": details_books.title,
        "author": details_books.author,
        "year": details_books.year,
        "isbn": isbn,
        "review_count": reviews_count,
        "average_score": average_rating
    })
