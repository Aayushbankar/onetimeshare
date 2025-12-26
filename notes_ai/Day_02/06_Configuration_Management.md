# 06. Configuration Management in Flask

## The Problem: Hardcoded Values

```python
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024
REDIS_HOST = 'localhost'
```

What's wrong?
1. **Different environments need different values**: `localhost` in dev, `redis` in Docker
2. **Secrets in code**: API keys end up in Git history
3. **No central place**: Constants scattered across files

---

## Flask's Configuration System

Flask has a built-in `config` object:

```python
# Accessing config
app.config['DEBUG']
app.config['SECRET_KEY']

# Setting config
app.config['UPLOAD_FOLDER'] = '/var/uploads'
```

---

## Method 1: Environment Variables (Best for Production)

**Setting environment variables:**
```bash
export REDIS_HOST=redis
export MAX_UPLOAD_SIZE=10485760
```

**Reading in Flask:**
```python
import os

def create_app():
    app = Flask(__name__)
    
    app.config['REDIS_HOST'] = os.environ.get('REDIS_HOST', 'localhost')
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_SIZE', 10485760))
    
    return app
```

---

## Method 2: Configuration Classes

Create a `config.py` file:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class DockerConfig(Config):
    REDIS_HOST = 'redis'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'docker': DockerConfig
}
```

**Loading config:**
```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app
```

---

## The `current_app` Proxy

Inside route handlers, use `current_app`:

```python
from flask import current_app

@bp.route('/upload', methods=['POST'])
def upload():
    upload_folder = current_app.config['UPLOAD_FOLDER']
```

---

## Best Practices

### Never Commit Secrets
Use `.env` file (add to `.gitignore`):

```bash
# .env
SECRET_KEY=super-secret-key
DATABASE_URL=postgresql://...
```

### Type Conversion
Environment variables are strings:

```python
# Convert to int
MAX_SIZE = int(os.environ.get('MAX_SIZE', 10485760))

# Convert to bool
DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', '1')
```

---

## Practice Exercises

1. Create `config.py` with configuration classes
2. Install `python-dotenv` and load from `.env`
3. Add validation for required config values
