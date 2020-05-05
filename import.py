import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://ukiqyxpjytmnqk:752de8d60c9db6736c5d9d6a7972a70228fad45de4dc1b466833f93108bcd018@ec2-79-125-26-232.eu-west-1.compute.amazonaws.com:5432/d23cjhe2n1foda"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    # db.drop_all()
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader,None)
    for isbn, title, author, year in reader:
        book = Books(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print(f"You just added {title} to the database (ISBN: {isbn}, author: {author} and year: {year}).")
    db.session.commit()
    print(f"DONE!")

if __name__ == "__main__":
    with app.app_context():
        main()
