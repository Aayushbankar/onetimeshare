# 03. Python Imports & Project Structure

## The "Shadowing" Trap
One of your errors today was creating a file named `app/app.py`.
This is a classic Python trap.

### How Python Imports Work
When you type `from app import create_app`:
1.  Python looks for a folder named `app`.
2.  It checks if it has an `__init__.py`. If yes, it treats `app` as a **package**.
3.  It executes `__init__.py`.
4.  It expects to find `create_app` inside that package context.

### The Conflict
If you have:
```
/project
  run.py
  /app           <-- Package
    __init__.py
    app.py       <-- Module
```

If you do `from app import app` inside `run.py`:
- Python might see the folder `app` (package).
- Inside `run.py`, you might effectively be asking for the `app` **module** (the file `app.py`) inside the `app` **package**.
- Since your `app.py` was empty, it didn't have the things you were looking for.

### Naming Conventions
- **Never name a file `email.py`**: It breaks the built-in `email` library.
- **Never name a file `code.py`**: It breaks the built-in `code` library.
- **Avoid `app.py` inside a package named `app`**: It is confusing (`app.app`).

## Correct Structure
Your corrected structure is perfect:
```
/onetimeshare
  run.py             # Entry point (Script)
  /app               # The Package
    __init__.py      # The Factory (exports create_app)
    routes.py        # Views (to be added)
    models.py        # Database (to be added)
```

### `__init__.py` Powers
This file is magical. It can:
1.  Mark a directory as a package.
2.  Expose internal function to the outside world.
    - If `app/routes.py` has a function `xyz`, `app/__init__.py` can import it, and then `run.py` can just do `from app import xyz`. It "flattens" your structure for consumers.
