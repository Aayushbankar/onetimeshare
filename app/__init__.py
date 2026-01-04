#  task create a The Application Factory 

import os
import redis
from flask import Flask
from . import routes 
import config

CONFIG  = config.Config()

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
        
        redis_service = RedisService(Config.REDIS_HOST, Config.REDIS_PORT)
        
        # Clean up orphaned files (files without metadata)
        file_result = redis_service.cleanup_orphan_files()
        app.logger.info(f"Startup file cleanup: {file_result}")
        
        # Clean up orphaned metadata (metadata without files)
        metadata_result = redis_service.cleanup_orphan_metadata()
        app.logger.info(f"Startup metadata cleanup: {metadata_result}")
        
        # Reset analytics counters on startup (prevent stale data from Redis persistence)
        analytics_counters = [
            "uploads", "downloads", "deletions",
            "index_visits", "list_files_visits", "info_visits",
            "protected_downloads", "unprotected_downloads"
        ]
        for counter in analytics_counters:
            redis_service.set_counter(counter, 0)
        app.logger.info(f"Startup analytics reset: {len(analytics_counters)} counters reset to 0")

    
    return app

