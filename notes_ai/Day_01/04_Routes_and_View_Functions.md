# 04. Routes & View Functions

## The Anatomy of a Route
```python
@app.route('/hello')
def hello():
    return 'Hello, World!'
```

### 1. The Decorator (`@app.route`)
In Python, `@` denotes a decorator. A decorator is a function that takes *another function* and modifies it or registers it.
- Here, `@app.route` tells Flask: "Hey, keep this function `hello` in your list. If someone asks for URL `/hello`, run this function."

### 2. The View Function (`def hello():`)
This is standard Python. It can do anything: calculate math, query a database, call an API.
- **Requirement**: It MUST return something that can be turned into an HTTP Response (string, HTML, JSON, or a tuple).

### 3. Variable Rules (Dynamic URLs)
You don't just want static pages. You want dynamic ones.
```python
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {username}'
```
- `<username>` matches any text.
- That text is passed as an argument to the function.
- You can specify types: `<int:post_id>`, `<uuid:id>`.

## Organizing Routes (Blueprints)
Right now, you are defining routes inside `create_app` (or `__init__.py`).
**This will not scale.** You don't want a 5000-line `__init__.py`.

**Tomorrow's Topic: Blueprints**.
Blueprints allow you to define routes in separate files (`routes.py`) and "register" them with the app factory. usage:
```python
# app/routes.py
from flask import Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index(): ...
```
```python
# app/__init__.py
def create_app():
    app = Flask(__name__)
    from . import routes
    app.register_blueprint(routes.bp)
    return app
```
You will likely implement this next.
