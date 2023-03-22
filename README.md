# FastAPI minimal project setup

This project is a minimal setup for a fastapi project configured with sqlalchemy ORM for RDBMS integration and a user authentication and authorization, login and basic CRUD operations on the user object.

I came up with this to save me the stress of the whole initial project setup processes. I guess I'm that lazy.

---

## Project setup

To install, git clone the project
```bash
git clone https://github.com/GeeNahz/fastapi-minimal-setup.git
```

---

Create a virtual environment in the base folder
```bash
pythom3 -m venv env
```
and activate it
```bash
source env/bin/activete
```

---

Then install the libraries
```bash
pip install -r requirements.txt
```

---


Finally, run the app
```bash
uvicorn app.main:app --reload
```

