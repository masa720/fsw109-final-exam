from flask import Flask, request, jsonify
import os
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


def user_to_dict(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


def author_to_dict(author: Author):
    return {
        "id": author.id,
        "name": author.name,
    }


def book_to_dict(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "author_id": book.author_id,
    }



@app.route("/")
def index():
    return "Hello!"


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"error": "email already exists"}), 400

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify(user_to_dict(user)), 201


@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    result = [user_to_dict(u) for u in users]
    return jsonify(result), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    return jsonify(user_to_dict(user)), 200


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if name:
        user.name = name

    if email:
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "email already in use by another user"}), 400
        user.email = email

    db.session.commit()

    return jsonify(user_to_dict(user)), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"user {user_id} deleted"}), 200


# Author CRUD

@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()

    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    author = Author(name=name)
    db.session.add(author)
    db.session.commit()

    return jsonify(author_to_dict(author)), 201


@app.route("/authors", methods=["GET"])
def get_all_authors():
    authors = Author.query.all()
    result = [author_to_dict(a) for a in authors]
    return jsonify(result), 200


@app.route("/authors/<int:author_id>", methods=["GET"])
def get_author_by_id(author_id):
    author = Author.query.get(author_id)
    if not author:
        return jsonify({"error": "author not found"}), 404

    return jsonify(author_to_dict(author)), 200


@app.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return jsonify({"error": "author not found"}), 404

    books = Book.query.filter_by(author_id=author_id).all()
    result = [book_to_dict(b) for b in books]
    return jsonify(result), 200


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    title = data.get("title")
    author_id = data.get("author_id")

    if not title or not author_id:
        return jsonify({"error": "title and author_id are required"}), 400

    author = Author.query.get(author_id)
    if not author:
        return jsonify({"error": "author not found"}), 404

    book = Book(title=title, author_id=author_id)
    db.session.add(book)
    db.session.commit()

    return jsonify(book_to_dict(book)), 201


@app.route("/books", methods=["GET"])
def get_all_books():
    author_id = request.args.get("author_id", type=int)

    if author_id is not None:
        books = Book.query.filter_by(author_id=author_id).all()
    else:
        books = Book.query.all()

    result = [book_to_dict(b) for b in books]
    return jsonify(result), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "book not found"}), 404

    return jsonify(book_to_dict(book)), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": f"book {book_id} deleted"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
