import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ukiqyxpjytmnqk:752de8d60c9db6736c5d9d6a7972a70228fad45de4dc1b466833f93108bcd018@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d23cjhe2n1foda"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Index page for sign-in or sign-up
@app.route("/")
def index():
    return render_template("index.html")

# Page for sign-up
@app.route("/register")
def register():
    """get information from user"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    """check if information is valid"""

    """add username and password to database"""


    return render_template("register.html",email=email,password=password)

# Home page with search bar and book list
@app.route("/home")
def home():
    """get log-in information from user"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    """check if username and password match database"""
    list_books = Books.query.all()
    
    return render_template("home.html",list_books=list_books)



@app.route("/book")
def book():
    """list details of books"""
    isbn = "0590554107"
    details_books = Books.query.get(isbn)

    """list reviews from users"""

    """list reviews from Goodread"""


    return render_template("book.html",details_books=details_books)

@app.route("/api")
def api():
    return "To do"

