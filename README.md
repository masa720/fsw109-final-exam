# Flask Library Management System

This project is a Library Management System built using Flask and SQLAlchemy.
It was created as part of the FSW109 Final Exam requirements.

The application models four related entities:

- User
- Author
- Book
- Borrow

It implements CRUD operations for each model, as required by the assignment.

---

## Features

### User CRUD
- Create a new user
- Retrieve all users
- Retrieve a user by ID
- Update a user
- Delete a user

### Author CRUD
- Add a new author
- Retrieve all authors
- Retrieve all books written by an author

### Book CRUD
- Add a new book
- Retrieve all books
- Retrieve books by author
- Delete a book

### Borrow CRUD
- Create a borrow record (borrow a book)
- Retrieve all borrowed books for a user
- Retrieve all users who borrowed a specific book

---

## Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd fsw109-final-exam
```

### 2. Create and activate a virtual environment (macOS/zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> If you already have a `venv/` folder, you can use it instead:
> `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

- The server starts at: http://127.0.0.1:5000/
- A SQLite database file (`library.db`) will be created automatically.
- If port 5000 is already in use, specify another port:

```bash
PORT=5001 python main.py
```

---

## API Endpoints

### User
| Method | Endpoint            | Description           |
|--------|---------------------|-----------------------|
| POST   | /users              | Create a new user     |
| GET    | /users              | Get all users         |
| GET    | /users/{id}         | Get a user by ID      |
| PUT    | /users/{id}         | Update a user         |
| DELETE | /users/{id}         | Delete a user         |

### Author
| Method | Endpoint                 | Description                      |
|--------|--------------------------|----------------------------------|
| POST   | /authors                 | Add a new author                 |
| GET    | /authors                 | Get all authors                  |
| GET    | /authors/{id}/books      | Get books written by an author   |

### Book
| Method | Endpoint                 | Description                           |
|--------|--------------------------|---------------------------------------|
| POST   | /books                   | Add a new book                        |
| GET    | /books                   | Get all books                         |
| GET    | /books?author_id={id}    | Get books filtered by author          |
| GET    | /books/{id}              | Get a book by ID                      |
| DELETE | /books/{id}              | Delete a book                         |

### Borrow
| Method | Endpoint                    | Description                               |
|--------|-----------------------------|-------------------------------------------|
| POST   | /borrows                    | Create a borrow record                    |
| GET    | /users/{id}/borrows         | Get books borrowed by a user              |
| GET    | /books/{id}/borrowers       | Get users who borrowed a specific book    |

