#  task create a The Application Factory 

import os
import redis
from flask import Flask
from . import routes 
import config

from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Initialize extensions (no SQLAlchemy needed!)
login_manager = LoginManager()
jwt = JWTManager()

CONFIG = config.Config()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    redis_client = redis.Redis(host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=0, decode_responses=True)
    app.redis_client = redis_client
    app.config.from_object(CONFIG)
    app.register_blueprint(routes.bp)
    
    with app.app_context():
        from app.services.redis_service import RedisService
        from config import Config
        import time
        
        # Retry Redis connection (Docker network may not be ready immediately)
        redis_service = None
        # Before the retry loop (line 32):
        time.sleep(3)  # Wait for Docker DNS to be ready
        for attempt in range(5):
            try:
                redis_service = RedisService(Config.REDIS_HOST, Config.REDIS_PORT)
                # Test connection
                redis_service.redis_client.ping()
                app.logger.info(f"✅ Redis connected: {Config.REDIS_HOST}:{Config.REDIS_PORT}")
                break
            except Exception as e:
                app.logger.warning(f"Redis connection attempt {attempt + 1}/5 failed: {e}")
                if attempt < 4:
                    time.sleep(2)  # Wait 2 seconds before retry
        
        if redis_service:
            # Clean up orphaned files (files without metadata)
            file_result = redis_service.cleanup_orphan_files()
            app.logger.info(f"Startup file cleanup: {file_result}")
            
            # Clean up orphaned metadata (metadata without files)
            metadata_result = redis_service.cleanup_orphan_metadata()
            app.logger.info(f"Startup metadata cleanup: {metadata_result}")
            
            # Reset analytics counters on startup
            analytics_counters = [
                "uploads", "downloads", "deletions",
                "index_visits", "list_files_visits", "info_visits",
                "protected_downloads", "unprotected_downloads"
            ]
            for counter in analytics_counters:
                redis_service.set_counter(counter, 0)
            app.logger.info(f"Startup analytics reset: {len(analytics_counters)} counters reset to 0")
        else:
            app.logger.error("❌ Could not connect to Redis after 5 attempts!")
        
        # Check admin credentials configured
        if not Config.ADMIN_PASSWORD:
            app.logger.warning("⚠️ ADMIN_PASSWORD not set! Admin login disabled.")
        else:
            app.logger.info(f"✅ Admin configured: {Config.ADMIN_USERNAME}")

    # Initialize extensions with app
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in.'
    
    # User loader - returns a simple admin object
    @login_manager.user_loader
    def load_user(user_id):
        from app.auth.admin_user import AdminUser
        if user_id == 'admin':
            return AdminUser()
        return None
    
    # Register auth blueprint
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/admin')
    
    # Security: Auto-logout admin when leaving /admin routes
    # Prevents session hijacking by limiting session scope
    @app.before_request
    def auto_logout_non_admin_routes():
        from flask_login import current_user, logout_user
        from flask import request
        
        # Only check if user is authenticated
        if current_user.is_authenticated:
            # Allow /admin routes and static files
            allowed_prefixes = ('/admin', '/static', '/stats', '/list-files')
            if not request.path.startswith(allowed_prefixes):
                logout_user()
                app.logger.info(f"Auto-logout: Admin left protected area ({request.path})")

    return app
