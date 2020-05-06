import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    books_review = db.relationship("Reviews", backref="book", lazy=True)

class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    reviews_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
    reviews_username = db.Column(db.String, db.ForeignKey("users.username"), nullable=False)

class Users(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
