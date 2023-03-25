from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)0
    isbn = db.Column(db.String, nullable=False)1
    title = db.Column(db.String, nullable=False)2
    author = db.Column(db.String, nullable=False)3
    year = db.Column(db.String, nullable=False)4


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)