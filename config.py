import os 
import secrets
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 mb
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif','env','md'}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 mb
    REDIS_TTL = 5 * 60 * 60  # 5 hours

    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

    # Password configs 
    MAX_PASSWORD_LENGTH = 128
    MIN_PASSWORD_LENGTH = 8
    MAX_RETRIES = 5

    # ===== ADMIN AUTH (Config-Based) =====
    # Set these in .env file. No database needed!
    # Admin credentials are loaded ONCE at startup.
    # To add/change admin: modify .env and restart server.
    
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', None)  # Plain text in .env
    
    # JWT for API access
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    @classmethod
    def verify_admin(cls, username, password):
        """Verify admin credentials against config."""
        if not cls.ADMIN_PASSWORD:
            return False
        return (
            secrets.compare_digest(username, cls.ADMIN_USERNAME) and 
            secrets.compare_digest(password, cls.ADMIN_PASSWORD)
        )

    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 64 * 1024))  # 64KB



    ARGON2_MEMORY_COST = int(os.environ.get("ARGON2_MEMORY_COST", 65536))
    ARGON2_TIME_COST = int(os.environ.get("ARGON2_TIME_COST", 3))
    ARGON2_PARALLELISM = int(os.environ.get("ARGON2_PARALLELISM", 4))
    ARGON2_SALT_LENGTH = int(os.environ.get("ARGON2_SALT_LENGTH", 16))



    # rate-limiting :
    RATELIMIT_STORAGE_URI = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', 6379)}/0"
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'true').lower() == 'true'



    SESSION_COOKIE_HTTPONLY = True
    # Only require HTTPS in production. Default to False for local dev.
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'