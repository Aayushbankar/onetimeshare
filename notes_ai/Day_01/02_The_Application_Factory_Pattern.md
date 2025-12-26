# 02. The Application Factory Pattern

## The "Global App" Problem
In simple tutorials, you often see this:
```python
# app.py
app = Flask(__name__)

@app.route('/')
def index(): ...

if __name__ == '__main__':
    app.run()
```
This puts the `app` object in the **global scope**. 

### Why is this bad?
1.  **Testing**: If you want to test your app, you can't easily create a "fresh" copy of it. The global `app` is already stuck with whatever configuration it started with.
2.  **Circular Imports**: As your app grows, you split it into files. If `models.py` imports `app`, and `app` imports `models.py`, Python crashes.
3.  **Multiple Instances**: You can't run two versions of your app with different settings in the same process.

## The Solution: The Factory Function
Instead of creating the app *immediately* at the top level, we write a function that creates it *on demand*.

```python
# app/__init__.py
def create_app(config=None):
    app = Flask(__name__)
    
    # Do setup here (register routes, db, etc.)
    
    return app
```

### How it works in your code
1.  **In `app/__init__.py`**: You defined `create_app`. It prepares the Flask object but doesn't run it.
2.  **In `run.py`**: You are the "Manager". You import the factory (`create_app`) and call it (`app = create_app()`).

This separation of concerns is pro-level engineering. The `app/__init__.py` defines *what* the app is. The `run.py` defines *how* to run it.

## Key Concept: Applications Context
When using a factory, there isn't always an "active" application.
- `current_app`: A special proxy in Flask that points to the handling application.
- You will see this later. If you try to use `app.config` outside of a request, it might fail because "app" doesn't exist globally!
