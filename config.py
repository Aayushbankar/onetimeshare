import os 

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = os.path.abspath(os.environ.get('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 mb
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')  # Default is 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif','env'}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 mb
    REDIS_TTL = 5 * 60 * 60  # 5 hours

    BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
