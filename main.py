from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    borrowed_books = db.relationship(
        "Borrow",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", back_populates="books")

    borrows = db.relationship(
        "Borrow",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class Borrow(db.Model):
    __tablename__ = "borrows"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="borrowed_books")

    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    book = db.relationship("Book", back_populates="borrows")

    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def index():
    return "Hello!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
