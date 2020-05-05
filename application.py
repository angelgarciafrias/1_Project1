import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://ukiqyxpjytmnqk:752de8d60c9db6736c5d9d6a7972a70228fad45de4dc1b466833f93108bcd018@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d23cjhe2n1foda")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return "Project 1: TODO"
