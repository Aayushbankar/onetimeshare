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
    
    return app