import os

from flask import Flask, render_template, request, session
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
        if not (request.form.get("username") or request.form.get("password") or request.form.get("email")):
            return render_template("error.html", message="You must provide all the information")

        """check if username is valid"""
        username_check = Users.query.get(request.form.get("username"))
        if username_check:
            return render_template("error.html", message="Username already taken.")

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
    list_books = Books.query.all()
    return render_template("home.html",list_books=list_books)



@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    """list details of books"""
    details_books = Books.query.get(isbn)


    
    """list reviews from Goodread"""

    current_user = session["username_session"]
    """submit review"""
    if request.method == "POST":
        check_reviews = Reviews.query.filter_by(reviews_isbn=isbn,reviews_username=current_user).first()
        if check_reviews:
            return render_template("error.html", message="You have already submitted a review for this book.")
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

    return render_template("book.html",details_books=details_books,list_reviews=list_reviews,current_user=current_user)

@app.route("/api")
def api():
    return render_template("error.html", message="Pendiente")

