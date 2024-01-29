# FastAPI minimal project setup

This project is a minimal setup for a fastapi projects that provides a boilerplate for commonly used backend/API features 

> This saves me the hassle of the whole initial project setup processes. I guess I'm that lazy😅.

---

## Features
* Authentication and authorisation
* User login and logout
* CRUD operations on a basic user model
* SQLAlchemy ORM for database abstraction
* Alembic for database migrations management


## Upcoming features
* Password reset


## Project setup
Clone the repository
```bash
git clone https://github.com/GeeNahz/fastapi-minimal-setup.git
```

---

Create a virtual environment in the base folder
```bash
$ pythom3 -m venv env
```
and activate it
```bash
$ source env/bin/activate
```

---

Then install the libraries
```bash
$ pip install -r requirements.txt
```

---


Finally, run the app
```bash
$ uvicorn app.main:app --reload
```

