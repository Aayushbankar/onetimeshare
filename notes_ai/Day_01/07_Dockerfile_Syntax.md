# 07. Dockerfile Syntax & Best Practices

A `Dockerfile` is a text document that contains all the commands a user could call on the command line to assemble an image.

## The Essential Commands

### 1. `FROM`
**Must be the first line.** Defines the base image.
```dockerfile
FROM python:3.13-slim
```
*Tip: Always use specific tags (`3.13-slim`) instead of `latest` or just `python`. `alpine` is smaller but uses a different C-library (musl) which causes headaches for Python data science packages. `slim` (Debian-based) is the safe bet.*

### 2. `WORKDIR`
Sets the working directory inside the container. Like `cd`.
```dockerfile
WORKDIR /app
```
*Rule: Always set this early. Don't work in the root `/` folder.*

### 3. `COPY` vs `ADD`
Moves files from your computer (host) to the container.
```dockerfile
COPY requirements.txt .
```
*Best Practice: Use `COPY`. `ADD` has extra features (downloading URLs, unzipping tars) which can be dangerous/unpredictable.*

### 4. `RUN`
Executes a command *during the build process*. This creates a new layer.
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
*Tip: Chain commands with `&&` to reduce layers, but newer Docker handles this better. The `--no-cache-dir` flag keeps the image small by deleting cached pip files.*

### 5. `CMD` vs `ENTRYPOINT`
Tells the container what to do when it starts.
```dockerfile
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
```
*Syntax: Use the JSON array format `["cmd", "arg"]`. It's safer.*

## The "Golden Order" for Caching
Docker stops caching at the first line that changes.
**WRONG:**
```dockerfile
COPY . .                  # Copies code (changes often)
RUN pip install -r requirements.txt # Now this re-runs every time code changes!
```

**RIGHT:**
```dockerfile
COPY requirements.txt .   # Only changes when deps change
RUN pip install ...       # Cached 99% of the time!
COPY . .                  # Copies code
```
This optimization saves you minutes on every build.
