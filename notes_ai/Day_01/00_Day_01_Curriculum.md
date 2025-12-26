# Day 01: Flask Fundamentals, Architecture & Docker

## Curriculum Overview
Today's session focuses on building a robust mental model of how Flask works and introducing Containerization with Docker.

### Topics Covered
#### Part 1: Flask (Completed)
1.  **Flask Architecture**: What actually is Flask? (WSGI, Werkzeug, Jinja2).
2.  **The Application Factory Pattern**: Why we don't just use a global `app` variable.
3.  **Python Imports & Structure**: How Python finds your code and why file naming matters (`app.py` vs `__init__.py`).
4.  **Routing & Views**: How a URL becomes a function call.
5.  **Mistake Analysis**: A breakdown of the specific errors encountered today and how to spot them in the future.

#### Part 2: Docker (New!)
6.  **Docker Mental Model**: Images vs Containers, Layers, and why VMs are different.
7.  **Dockerfile Syntax**: Deep dive into `FROM`, `COPY`, `RUN`, `CMD` and the "Golden Order" for caching.
8.  **Real World Workflow**: How to avoid rebuilding images constantly using Volumes and Docker Compose.

## How to use these notes
Read the files in numerical order. Each file builds upon the concepts of the previous one.
