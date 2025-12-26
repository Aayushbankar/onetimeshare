# 01. Flask Architecture & Theory

## What is Flask?
Flask is classified as a **microframework**. This doesn't mean it's "small" in terms of what it can do; it means the *core* is kept simple and extensible. It does not force decisions upon you (like which database to use or how to validate forms).

### The "Trinity" of Flask
Flask is actually a wrapper around two other important libraries:
1.  **Werkzeug** (The "Workhorse"): A comprehensive WSGI web application library. It handles the low-level stuff:
    -   Parsing URLs (Routing).
    -   Handling Request/Response objects.
    -   Debugging.
2.  **Jinja2** (The "Artist"): A templating engine. It lets you mix Python-like logic (loops, variables) into your HTML files.
3.  **Click** (The "Command Line"): Used for creating command-line interfaces (like the `flask run` command).

## The Request-Response Cycle (The Life of a Request)
Understanding this cycle is crucial. When you hit `http://localhost:5000/`:

1.  **The Request**: Your browser sends an HTTP request (GET /) to the server.
2.  **WSGI Layer**: The web server (in dev, `werkzeug`; in prod, `gunicorn`) receives this raw text and converts it into a Python object called the `environ`.
3.  **Flask Routing**: Flask looks at the URL (`/`) and checks its **URL Map**. It finds that `/` matches the function `hello()`.
4.  **View Function**: Flask calls your `hello()` function.
    -   *Crucial Point*: You don't call this function. Flask calls it. This is "Inversion of Control".
5.  **Return Value**: Your function returns a string "Hello, World!".
6.  **Response Creation**: Flask wraps this string into a full HTTP Response object (adding headers like `Content-Type: text/html`, status code `200 OK`).
7.  **The Response**: This object is converted back to raw bytes and sent to your browser.

## Why this matters
Knowing this helps you debug.
- If you get a 404, the **Routing** step failed (URL Map didn't match).
- If you get a 500, the **View Function** crashed.
- If the browser sees weird characters, the **Response Creation** (headers) might be wrong.
